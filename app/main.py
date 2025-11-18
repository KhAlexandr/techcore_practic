import asyncio

import datetime
import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from opentelemetry.instrumentation.aiokafka import AIOKafkaInstrumentor
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from app.routers import books, reviews
from app.celery_tasks.worker_service import router
from app.kafka_conf.producer import get_producer
from app.open_telemetry import setup_tracing
from app.database import engine
from app.kafka_conf.consumer import AnalyticsWorker
from app.logging import logger
from app.routers.author_service import router as author_router


setup_tracing("book-service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    background_service = books.BackgroundService()
    analytics_worker = AnalyticsWorker()
    task = asyncio.create_task(background_service.cache_listener())
    producer = await get_producer()
    await producer.start()
    task1 = asyncio.create_task(analytics_worker.book_view())
    yield
    task.cancel()
    task1.cancel()
    await producer.stop()


app = FastAPI(lifespan=lifespan)


FastAPIInstrumentor.instrument_app(app)
SQLAlchemyInstrumentor().instrument(engine=engine.sync_engine)
CeleryInstrumentor().instrument()
AIOKafkaInstrumentor().instrument()


@app.middleware("http")
async def logs(request: Request, call_next):
    logger.info(
        "http_request",
        method=request.method,
        url=str(request.url),
        path=request.url.path,
        query_params=dict(request.query_params),
    )
    response = await call_next(request)
    logger.info(
        "http_response",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        response_size=response.headers.get("content-length", 0),
    )
    return response


@app.get("/")
async def hello():
    await asyncio.sleep(1)
    return {"message": "Hello, World"}


@app.get("/healthz")
async def health_check():
    return {"status": "healthy"}


@app.get("/metrics")
async def metrics_endpoint():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


app.include_router(books.router)
app.include_router(reviews.reviews_router)
app.include_router(router)
app.include_router(author_router)


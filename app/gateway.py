import asyncio

import httpx
import pybreaker
from fastapi import Depends, FastAPI, Response
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.auth import verify_user
from app.books.schemas import BookScheme
from app.breaker import detail_breaker
from app.logging import logger
from app.open_telemetry import setup_metrics, setup_tracing

setup_tracing("gateway-service")
setup_metrics("gateway-service")

app = FastAPI()

FastAPIInstrumentor.instrument_app(app)
HTTPXClientInstrumentor().instrument()

logger.info("service_started", service_name="gateway")

tracer = trace.get_tracer(__name__)


@app.get("/metrics")
async def metrics_endpoint():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/healthz")
async def health_check():
    return {"status": "healthy"}


@app.get("/getaway/api/books/{book_id}")
async def get_book(book_id: int, user: dict = Depends(verify_user)):
    async with httpx.AsyncClient() as client:
        try:
            headers = {"Authorization": f"Bearer {user.get('token', '')}"}
            response = await client.get(
                f"http://api:80/api/books/{book_id}", timeout=10.0, headers=headers
            )
            return response.json()
        except Exception as e:
            return {"error": f"Ошибка Gateway: {str(e)}"}


#
# @app.get("/details/{id}")
# async def get_details(id: int):
#     async with httpx.AsyncClient() as client:
#         try:
#             task1 = asyncio.create_task(
#                 client.get(
#                     f"http://api:80/api/books/{id}",
#                     timeout=10.0,
#                 )
#             )
#             task2 = asyncio.create_task(
#                 client.get(f"http://api:80/api/api/products/{id}/reviews")
#             )
#             book, review = await asyncio.gather(task1, task2)
#             return {"book": book.json(), "review": review.json()}
#         except Exception as e:
#             return {"error": f"Ошибка Gateway: {str(e)}"}


async def _call_details_service(id):
    async with httpx.AsyncClient() as client:
        task1 = asyncio.create_task(
            client.get(f"http://api:80/api/books/{id}", timeout=10.0)
        )
        task2 = asyncio.create_task(
            client.get(f"http://api:80/api/products/{id}/reviews")
        )

        book, review = await asyncio.gather(task1, task2)
        book.raise_for_status()
        review.raise_for_status()

        return {"book": book.json(), "review": review.json()}


@app.get("/details/{id}")
async def get_details(id: int):
    try:
        result = await detail_breaker.call_async(_call_details_service, id)
        return result

    except pybreaker.CircuitBreakerError:
        return {"error": "Details service temporarily unavailable"}

    except Exception as e:
        return {"error": f"Service error: {str(e)}"}


@app.post("/book")
async def create_book(book: BookScheme):
    log = logger.bind(
        operation="create_book_via_gateway",
        book_title=book.title,
        author_id=book.author_id,
    )

    log.info("gateway_request_started")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://api:80/api/books/",
            json=book.model_dump(),
            headers={
                "Content-Type": "application/json",
            },
        )
        log.info(
            "book_service_response",
            status_code=response.status_code,
            response_time_ms=response.elapsed.total_seconds() * 1000,
        )
        log.info("book_created_successfully")
    return response.json()

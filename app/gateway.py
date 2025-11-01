from fastapi import FastAPI, Depends, Response
import httpx
import asyncio

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from app.auth import verify_user
from app.books.schemas import BookScheme
from app.open_telemetry import setup_tracing
from app.open_telemetry import setup_metrics
from app.logging import logger


setup_tracing("gateway-service")
setup_metrics("gateway-service")

app = FastAPI()

FastAPIInstrumentor.instrument_app(app)
HTTPXClientInstrumentor().instrument()

logger.info("service_started", service_name="gateway")


@app.get("/metrics")
async def metrics_endpoint():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


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


@app.get("/details/{id}")
async def get_details(id: int):
    async with httpx.AsyncClient() as client:
        try:
            task1 = asyncio.create_task(
                client.get(
                    f"http://api:80/api/books/{id}",
                    timeout=10.0,
                )
            )
            task2 = asyncio.create_task(
                client.get(f"http://api:80/api/api/products/{id}/reviews")
            )
            book, review = await asyncio.gather(task1, task2)
            return {"book": book.json(), "review": review.json()}
        except Exception as e:
            return {"error": f"Ошибка Gateway: {str(e)}"}


@app.post("/book")
async def create_book(book: BookScheme):
    log = logger.bind(
        operation="create_book_via_gateway",
        book_title=book.title,
        author_id=book.author_id
    )

    log.info("gateway_request_started")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://api:80/api/books/",
            json=book.model_dump(),
            headers={
                "Content-Type": "application/json",
            },
        )
        log.info("book_service_response",
                 status_code=response.status_code,
                 response_time_ms=response.elapsed.total_seconds() * 1000)
        log.info("book_created_successfully")
    return response.json()

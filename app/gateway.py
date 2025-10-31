from fastapi import FastAPI, Depends
import httpx
import asyncio

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

from app.auth import verify_user
from app.open_telemetry import setup_tracing


setup_tracing("gateway-service")

app = FastAPI()

FastAPIInstrumentor.instrument_app(app)
HTTPXClientInstrumentor().instrument()


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
                client.get(f"http://api:80/api/books/{id}", timeout=10.0,)
            )
            task2 = asyncio.create_task(
                client.get(f"http://api:80/api/api/products/{id}/reviews")
            )
            book, review = await asyncio.gather(task1, task2)
            return {"book": book.json(), "review": review.json()}
        except Exception as e:
            return {"error": f"Ошибка Gateway: {str(e)}"}

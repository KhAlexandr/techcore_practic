import asyncio

import backoff
import httpx
from aiocircuitbreaker import CircuitBreakerError, circuit
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.authors.models import Author
from app.authors.schemas import AuthorScheme
from app.database import get_db_session
from app.redis_database import redis_client

semaphore = asyncio.Semaphore(5)

router = APIRouter(prefix="/author", tags=["Управление авторами"])


class AuthorService:
    def __init__(self):
        self.client = None

    async def __aenter__(self):
        self.client = httpx.AsyncClient()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    @circuit(failure_threshold=5)
    @backoff.on_exception(backoff.expo, httpx.RequestError, max_tries=3)
    async def get_author(self, author_id):
        async with semaphore:
            task1 = self.client.get(f"http://api/author/{author_id}")
            task2 = self.client.get("http://review-service/")
            response = await asyncio.gather(task1, task2, return_exceptions=True)
            response_1 = response[0]
            response_1.raise_for_status()
            return response_1.json()

    async def get_author_name(self, author_id):
        try:
            author = await self.get_author(author_id)
            return author["name"]
        except CircuitBreakerError:
            return "Default Author"
        except Exception:
            return "Default Author"

    @circuit(failure_threshold=5)
    @backoff.on_exception(
        backoff.expo, (httpx.RequestError, asyncio.TimeoutError), max_tries=3
    )
    async def get_wait_for(self):
        response = await asyncio.wait_for(
            self.client.get("https://httpbin.org/delay/4"), timeout=1.0
        )
        return response.json()

    @staticmethod
    async def create_author(author: AuthorScheme, session: AsyncSession):
        new_author = Author(**author.model_dump())
        session.add(new_author)
        await session.commit()
        return new_author


@router.post("")
async def create_author(
    author: AuthorScheme,
    session: AsyncSession = Depends(get_db_session),
    author_service: AuthorService = Depends(AuthorService),
):
    new_autor = await author_service.create_author(author, session)
    return new_autor


@router.get("/wait_for")
async def get_timeout():
    async with AuthorService() as repo:
        try:
            await repo.get_wait_for()
        except CircuitBreakerError:
            author = await redis_client.get("author_id")
            if author is None:
                return "Default author"
            return author

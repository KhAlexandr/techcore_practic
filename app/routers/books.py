import asyncio
from typing import AsyncGenerator

import json

from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from opentelemetry import metrics

from app.authors.models import Author
from app.books.schemas import BookScheme
from app.books.models import Book
from app.database import get_db_session
from app.authors.schemas import AuthorScheme
from app.redis_database import redis_client
from app.kafka_conf.producer import view_book
from app.open_telemetry import setup_metrics
from app.logging import logger


meter_provider = setup_metrics("book-service")

meter = metrics.get_meter(__name__)

book_counter = meter.create_counter(
    name="books_created_total", description="Количество созданых книг", unit="1"
)

router = APIRouter(prefix="/api/books", tags=["Управление книгами"])


class BackgroundService:
    @staticmethod
    async def cache_listener():
        pubsub = redis_client.pubsub()
        await pubsub.subscribe("cache:invalidate")

        async for message in pubsub.listen():
            if message["type"] == "message":
                book_id = message["data"]
                await redis_client.delete(f"book:{book_id}")


class BookRepository:

    @staticmethod
    async def get_by_id(book_id: int, session: AsyncSession):
        key = f"book:{book_id}"
        cached_book = await redis_client.get(key)
        if cached_book:
            return json.loads(cached_book)
        result = await session.execute(
            select(Book).options(selectinload(Book.author)).where(Book.id == book_id)
        )
        book = result.scalar_one_or_none()
        if book:
            book_dict = book.to_dict()
            book_dict["author"] = {
                "id": book.author.id,
                "first_name": book.author.first_name,
                "last_name": book.author.last_name,
                "age": book.author.age,
            }
            await redis_client.set(key, json.dumps(book_dict))
            return book_dict
        return None

    @staticmethod
    async def get_all_books(session: AsyncSession):
        result = await session.scalars(select(Book))
        books = result.all()
        return [book.to_dict() for book in books]

    @staticmethod
    async def update_book(book_id: int, updated_book: BookScheme, session: AsyncSession,):
        async with redis_client.lock(f"inventory_lock:{book_id}", timeout=10):
            result = await session.execute(
                select(Book)
                .options(selectinload(Book.author))
                .where(Book.id == book_id)
            )
            book = result.scalar_one_or_none()
            if book:
                for key, value in updated_book.model_dump().items():
                    setattr(book, key, value)
                await session.commit()
                await redis_client.publish("cache:invalidate", str(book_id))
            return book

    @staticmethod
    async def create(
        book: BookScheme,
        session: AsyncSession,
    ) -> Book:
        book = Book(**book.model_dump())
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    @staticmethod
    async def create_author_and_book(
        book: BookScheme,
        author: AuthorScheme,
        session: AsyncSession,
    ):
        async with session.begin():
            author = Author(**author.model_dump())
            session.add(author)
            await session.flush()

            book = Book(**book.model_dump())
            session.add(book)
            return author


@router.get("/")
async def get_all_books(
        session: AsyncSession = Depends(get_db_session),
        book_repo: BookRepository = Depends(BookRepository)
):
    books = await book_repo.get_all_books(session=session)
    return {"books": books}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(
    book: BookScheme,
    session: AsyncSession = Depends(get_db_session),
    book_repo: BookRepository = Depends(BookRepository)
):
    log = logger.bind(operation="create_book", author_id=book.author_id)
    log.info("book_creation_started", title=book.title)
    new_book = await book_repo.create(
        book=book, session=session
    )
    log.info("book_created", book_id=new_book.id, title=new_book.title)
    book_counter.add(1, {"operation": "create", "author_id": str(book.author_id)})
    book_counter.add(1, {"operation": "create", "author_id": str(book.author_id)})
    asyncio.create_task(view_book(book_id=new_book.id))
    return {
        "id": new_book.id,
        "title": new_book.title,
        "year": new_book.year,
        "author_id": new_book.author_id,
    }


@router.get("/{book_id}")
async def get_book(
    book_id: int,
    session: AsyncSession = Depends(get_db_session),
    book_repo: BookRepository = Depends(BookRepository)
):
    book = await book_repo.get_by_id(book_id, session=session)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    asyncio.create_task(view_book(book_id=book_id))
    return {**book}


@router.patch("/{book_id}")
async def update_book(
    book_id: int,
    book: BookScheme,
    session: AsyncSession = Depends(get_db_session),
    book_repo: BookRepository = Depends(BookRepository)
):
    new_book = await book_repo.update_book(
        book_id=book_id,
        updated_book=book,
        session=session
    )
    if not new_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {**new_book.to_dict()}


@router.post("/create-author-and-book")
async def create_author_and_book(
    autor: AuthorScheme,
    book: BookScheme,
    session: AsyncSession = Depends(get_db_session),
    book_repo: BookRepository = Depends(BookRepository)
):
    new_author_and_book = await book_repo.create_author_and_book(
        book=book,
        author=autor,
        session=session,
    )
    return {
        "id": new_author_and_book.id,
        "first_name": new_author_and_book.first_name,
        "last_name": new_author_and_book.last_name,
        "age": new_author_and_book.age,
    }

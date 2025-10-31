from typing import AsyncGenerator

import json

from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.authors.models import Author
from app.books.schemas import BasBookScheme, BookScheme
from app.books.models import Book
from app.database import session_maker
from app.authors.schemas import AuthorScheme
from app.redis_database import redis_client
from app.routers.author_service import AuthorService
from app.kafka_conf.kafka_file import producer


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session


router = APIRouter(prefix="/api/books", tags=["Управление книгами"])


class BackgroundService:
    async def cache_listener(self):
        pubsub = redis_client.pubsub()
        await pubsub.subscribe("cache:invalidate")

        async for message in pubsub.listen():
            if message["type"] == "message":
                book_id = message["data"]
                await redis_client.delete(f"book:{book_id}")


class BookRepository:
    async def get_by_id(self, book_id: int, session: AsyncSession):
        key = f"book:{book_id}"
        cached_book = await redis_client.get(key)
        print(cached_book)
        if cached_book:
            return json.loads(cached_book)
        result = await session.execute(
            select(Book).options(selectinload(Book.author)).where(Book.id == book_id)
        )
        book = result.scalar_one_or_none()
        if book:
            author_service = AuthorService()
            author_name = await author_service.get_author_name(book.author_id)
            book_dict = book.to_dict()
            book_dict["author_name"] = author_name
            await redis_client.set(key, json.dumps(book_dict))
            return book_dict
        return None

    async def get_all_books(self, session: AsyncSession):
        result = await session.scalars(select(Book))
        books = result.all()
        return [book.to_dict() for book in books]

    async def update_book(self, book_id: int, session: AsyncSession, **kwargs):
        async with redis_client.lock(f"inventory_lock:{book_id}", timeout=10):
            result = await session.execute(
                select(Book)
                .options(selectinload(Book.author))
                .where(Book.id == book_id)
            )
            book = result.scalar_one_or_none()
            if book:
                for key, value in kwargs.items():
                    setattr(book, key, value)
                await session.commit()
                await redis_client.delete(f"book:{book_id}")
                await redis_client.publish("cache:invalidate", str(book_id))
            return book

    async def create(
        self,
        title: str,
        author_id: int,
        session: AsyncSession,
        year: int | None = None,
    ) -> Book:
        book = Book(title=title, year=year, author_id=author_id)
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    async def create_author_and_book(
        self,
        first_name: str,
        last_name: str,
        title: str,
        session: AsyncSession,
        age: int | None = None,
        year: int | None = None,
    ):
        async with session.begin():
            author = Author(first_name=first_name, last_name=last_name, age=age)
            session.add(author)
            await session.flush()

            book = Book(title=title, year=year, author_id=author.id)
            session.add(book)
            return author


book_repo = BookRepository()


@router.get("/")
async def get_all_books(session: AsyncSession = Depends(get_db_session)):
    books = await book_repo.get_all_books(session=session)
    return {"books": books}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(
    book: BookScheme, session: AsyncSession = Depends(get_db_session)
):
    new_book = await book_repo.create(
        title=book.title, year=book.year, author_id=book.author_id, session=session
    )
    await producer.send_and_wait(
        topic="book_views",
        key=str(new_book.id).encode("utf-8"),
        value=f"Создана новая книга с названием {new_book.title}".encode("utf-8"),
    )
    return {
        "id": new_book.id,
        "title": new_book.title,
        "year": new_book.year,
        "author_id": new_book.author_id,
    }


@router.get("/{book_id}")
async def get_book(
    book_id: int,
    background_task: BackgroundTasks,
    session: AsyncSession = Depends(get_db_session),
):
    book = await book_repo.get_by_id(book_id, session=session)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    await producer.send_and_wait(
        topic="book_views",
        key=str(book_id).encode("utf-8"),
        value=f"Книга {book['title']} была просмотрена.".encode("utf-8"),
    )
    return {**book}


@router.patch("/{book_id}")
async def update_book(
    book_id: int, book: BookScheme, session: AsyncSession = Depends(get_db_session)
):
    new_book = await book_repo.update_book(
        book_id=book_id,
        session=session,
        title=book.title,
        year=book.year,
        author_id=book.author_id,
    )
    if not new_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {**new_book.to_dict()}


@router.post("/create-author-and-book")
async def create_author_and_book(
    autor: AuthorScheme,
    book: BasBookScheme,
    session: AsyncSession = Depends(get_db_session),
):
    new_author_and_book = await book_repo.create_author_and_book(
        first_name=autor.first_name,
        last_name=autor.last_name,
        age=autor.age,
        title=book.title,
        year=book.year,
        session=session,
    )
    return {
        "id": new_author_and_book.id,
        "first_name": new_author_and_book.first_name,
        "last_name": new_author_and_book.last_name,
        "age": new_author_and_book.age,
    }

from typing import AsyncGenerator

from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.authors.models import Author
from app.books.schemas import BookScheme
from app.books.models import Book
from app.database import session_maker


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    async with session_maker() as session:
        yield session


router = APIRouter(prefix="/books", tags=["Упрпвление книгами"])


class BookRepository:
    async def get_by_id(self, book_id: int, session: AsyncSession):
        result = await session.execute(
            select(Book).options(selectinload(Book.author)).where(Book.id == book_id)
        )
        return result.scalar_one_or_none()

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


@router.post("/")
async def create_book(
    book: BookScheme, author_id: int, session: AsyncSession = Depends(get_db_session)
):
    new_book = await book_repo.create(
        title=book.title, year=book.year, author_id=author_id, session=session
    )
    return {"id": new_book.id, "title": new_book.title, "year": new_book.year}


@router.get("/{book_id}")
async def get_book(book_id: int, session: AsyncSession = Depends(get_db_session)):
    book = await book_repo.get_by_id(book_id, session=session)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"id": book_id, "title": book.title, "year": book.year}

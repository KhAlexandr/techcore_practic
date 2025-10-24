import asyncio

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select

from app.books.schemas import BookScheme
from app.books.models import Book
from app.database import session_maker


router = APIRouter(prefix="/books", tags=["Упрпвление книгами"])


class BookRepository:
    async def get_by_id(self, book_id: int):
        async with session_maker() as session:
            result = await session.execute(select(Book).where(Book.id == book_id))
            return result.scalar_one_or_none()

    async def create(self, title: str, year: int | None = None) -> Book:
        async with session_maker() as session:
            book = Book(title=title, year=year)
            session.add(book)
            await session.commit()
            await session.refresh(book)
            return book


book_repo = BookRepository()


@router.post("/")
async def create_book(book: BookScheme):
    new_book = await book_repo.create(title=book.title, year=book.year)
    return {"id": new_book.id, "title": new_book.title, "year": new_book.year}


@router.get("/{book_id}")
async def get_book(book_id: int):
    book = await book_repo.get_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=404, detail="Book not found"
        )
    return {"id": book_id, "title": book.title, "year": book.year}

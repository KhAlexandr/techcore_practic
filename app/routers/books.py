from fastapi import APIRouter, HTTPException

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.authors.models import Author
from app.books.schemas import BookScheme
from app.books.models import Book
from app.database import session_maker


router = APIRouter(prefix="/books", tags=["Упрпвление книгами"])


class BookRepository:
    async def get_by_id(self, book_id: int):
        async with session_maker() as session:
            result = await session.execute(
                select(Book)
                .options(selectinload(Book.author))
                .where(Book.id == book_id))
            return result.scalar_one_or_none()

    async def create(self, title: str, year: int | None = None) -> Book:
        async with session_maker() as session:
            book = Book(title=title, year=year)
            session.add(book)
            await session.commit()
            await session.refresh(book)
            return book

    async def create_author_and_book(
            self,
            first_name: str,
            last_name: str,
            title: str,
            age: int | None = None,
            year: int | None = None
    ):
        async with session_maker() as session:
            async with session.begin():
                author = Author(
                    first_name=first_name,
                    last_name=last_name,
                    age=age
                )
                session.add(author)
                await session.flush()

                book = Book(title=title, year=year, author_id=author.id)
                session.add(book)
                return author


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

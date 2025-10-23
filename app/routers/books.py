import asyncio

from fastapi import APIRouter, Depends, HTTPException

from app.books.models import BookScheme


router = APIRouter(prefix="/books", tags=["Упрпвление книгами"])


books_db = {}
current_id = 1


def get_db_session():
    session = books_db
    yield session


@router.post("/")
async def create_book(book: BookScheme, db: dict = Depends(get_db_session)):
    global current_id
    db[current_id] = book
    current_id += 1
    await asyncio.sleep(1)
    return {"id": current_id - 1, **book.dict()}


@router.get("/{book_id}")
async def get_book(book_id: int):
    await asyncio.sleep(1)
    if book_id not in books_db:
        raise HTTPException(
            status_code=404, detail="Book not found"
        )
    return {"id": book_id, **books_db[book_id].dict()}

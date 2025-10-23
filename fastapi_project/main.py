from fastapi import FastAPI, Depends

from books.models import BookScheme

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello, World"}


books_db = {}
current_id = 1


def get_db_session():
    session = books_db
    yield session


@app.post("/books")
def create_book(book: BookScheme, db: dict = Depends(get_db_session)):
    global current_id
    db[current_id] = book
    current_id += 1
    return {"id": current_id - 1, **book.dict()}


@app.get("/books/{book_id}")
def get_book(book_id: int):
    return {"id": book_id, **books_db[book_id].dict()}

from fastapi import FastAPI

from books.models import BookScheme

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello, World"}


books_db = {}
current_id = 1


@app.post("/books")
def post_book(book: BookScheme):
    global current_id
    books_db[current_id] = book
    current_id += 1
    return {"id": current_id - 1, **book.dict()}


@app.get("/books/{book_id}")
def get_book(book_id: int):
    return {"id": book_id, **books_db[book_id].dict()}

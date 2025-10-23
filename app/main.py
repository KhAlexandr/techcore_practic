from fastapi import FastAPI

from app.routers import books

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello, World"}


app.include_router(books.router)

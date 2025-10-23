import asyncio

from fastapi import FastAPI

from app.routers import books

app = FastAPI()


@app.get("/")
async def hello():
    await asyncio.sleep(1)
    return {"message": "Hello, World"}


app.include_router(books.router)

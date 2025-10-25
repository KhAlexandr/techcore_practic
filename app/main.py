import asyncio

import datetime
import logging

from fastapi import FastAPI, Request

from app.routers import books, reviews

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.middleware("http")
async def logs(request: Request, call_next):

    logger.info(f"{request.method}, {request.url}, {datetime.datetime.now()}")
    response = await call_next(request)
    return response


@app.get("/")
async def hello():
    await asyncio.sleep(1)
    return {"message": "Hello, World"}


app.include_router(books.router)
app.include_router(reviews.reviews_router)

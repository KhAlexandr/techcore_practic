import asyncio

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.mongo_database import mongo_client
from app.routers.books import BookRepository, get_db_session

from sqlalchemy.ext.asyncio import AsyncSession


book_repo = BookRepository()


reviews_router = APIRouter(prefix="/api", tags=["Управление отзыами"])


class ReviewScheme(BaseModel):
    product_id: int
    text: str


class ReviewService:
    def __init__(self):
        self.collection = mongo_client.db.reviews

    async def create_review(self, **kwargs):
        await self.collection.insert_one(kwargs)

    async def get_product_reviews(self, product_id: int):
        cursor = self.collection.find({"product_id": product_id})
        docs = [doc async for doc in cursor]
        for doc in docs:
            doc["_id"] = str(doc["_id"])
        return docs


review_service = ReviewService()


@reviews_router.post("/api/reviews")
async def create_review(review: ReviewScheme):
    await review_service.create_review(product_id=review.product_id, text=review.text)
    return dict(product_id=review.product_id, text=review.text)


@reviews_router.get("/api/products/{product_id}/reviews")
async def get_review(product_id: int):
    result = await review_service.get_product_reviews(product_id)
    return result


@reviews_router.get("/products/{product_id}/detail")
async def get_details(product_id: int, session: AsyncSession = Depends(get_db_session)):
    book_task = asyncio.create_task(book_repo.get_by_id(book_id=product_id, session=session))
    review_task = asyncio.create_task(review_service.get_product_reviews(product_id))
    book, review = await asyncio.gather(book_task, review_task)
    return {**book, "reviews": review}

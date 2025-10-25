from fastapi import APIRouter
from pydantic import BaseModel

from app.mongo_database import mongo_client


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

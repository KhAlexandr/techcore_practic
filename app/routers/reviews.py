from app.mongo_database import mongo_client


class ReviewService:
    def __init__(self):
        self.collection = mongo_client.db.reviews

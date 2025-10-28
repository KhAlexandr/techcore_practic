import time

from fastapi import APIRouter

from app.celery_apps import celery_app


router = APIRouter(prefix="/worker", tags=["Тестирование celery"])


class WorkerService:
    @celery_app.task(bind=True)
    def process_order(self, order_id):
        time.sleep(10)
        return order_id


worker = WorkerService()

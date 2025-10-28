import time

from fastapi import APIRouter, status

from app.celery_apps import celery_app


router = APIRouter(prefix="/order", tags=["Тестирование celery"])


class WorkerService:
    @celery_app.task(bind=True)
    def process_order(self, order_id):
        time.sleep(10)
        return order_id


worker = WorkerService()


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
def process_order(order_id: int):
    task = worker.process_order.delay(order_id)
    return {"task_id": task.id}

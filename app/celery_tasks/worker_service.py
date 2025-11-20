import time

from fastapi import APIRouter, status  # noqa: F401

from app.celery_tasks.celery_apps import celery_app

router = APIRouter(prefix="/order", tags=["Тестирование celery"])


@celery_app.task(
    bind=True, task_reject_on_worker_lost=True, acks_late=True, max_retries=3
)
def process_order(self, order_id):
    try:
        time.sleep(10)
        return order_id
    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)


# @router.post("/", status_code=status.HTTP_202_ACCEPTED)
# def process_order(order_id: int):
#     task = process_order.delay(order_id)
#     return {"task_id": task.id}

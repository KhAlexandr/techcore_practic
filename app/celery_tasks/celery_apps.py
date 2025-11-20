from celery import Celery

celery_app = Celery(
    "tasks",
    broker="pyamqp://guest:guest@rabbitmq:5672//",
    backend="redis://redis:6379/0",
)


@celery_app.task
def nightly_report():
    print("Nightly report executed!")
    return "Report completed"


celery_app.conf.beat_schedule = {
    "nightly-report": {
        "task": "app.celery_tasks.celery_apps.nightly_report",
        "schedule": 300.0,
    },
}

import app.celery_tasks.worker_service  # noqa

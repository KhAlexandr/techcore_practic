from celery import Celery

from dotenv import load_dotenv

import os

load_dotenv()


celery_app = Celery(
    "celery_tasks",
    backend="redis://localhost:6379/0",
    broker=f"pyamqp://{os.getenv('RABBITMQ_DEFAULT_USER')}:{os.getenv('RABBITMQ_DEFAULT_PASS')}@localhost:5672//"
)

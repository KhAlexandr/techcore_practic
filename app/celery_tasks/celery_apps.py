from celery import Celery

from dotenv import load_dotenv

import os

load_dotenv()


celery_app = Celery(
    'celery_tasks',
    broker=f'pyamqp://{os.getenv("RABBITMQ_DEFAULT_USER")}:{os.getenv("RABBITMQ_DEFAULT_PASS")}@rabbitmq:5672//',
    backend='redis://redis:6379/0',
)

import app.celery_tasks.worker_service

from celery import Celery
from core.config import settings


celery_app = Celery("worker", broker=settings.rabbitmq_url, include=["tasks"],)
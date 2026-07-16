from celery import Celery
from core.config import settings

celery_app = Celery("api_service", broker=settings.rabbitmq_url)

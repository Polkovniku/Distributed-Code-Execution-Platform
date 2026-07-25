from celery import Celery
from core.config import settings


celery_app = Celery("worker", broker=settings.rabbitmq_url, include=["tasks"],)

celery_app.conf.beat_schedule = {
    "cleanup-old-jobs": {
        "task": "cleanup_old_jobs",
        "schedule": 60.0, 
    },
}
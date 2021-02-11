from celery import Celery
from dotenv import load_dotenv, find_dotenv
import os
from datetime import timedelta

load_dotenv(find_dotenv())

broker = os.getenv("CELERY_BROKER", "redis://localhost:6379/0")
backend = os.getenv("CELERY_BACKEND", "redis://localhost:6379/0")
celery_app = Celery("converter", broker=broker, backend=backend)

celery_app.conf.beat_schedule = {
    "convert-audio-test": {
        "task": "test",
        "schedule": timedelta(seconds=5),
    }
}

@celery_app.task
def test():
    print("Hola mundo")

test.delay()
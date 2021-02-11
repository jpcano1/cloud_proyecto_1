from celery import Celery
from dotenv import load_dotenv, find_dotenv
import os
from datetime import timedelta

load_dotenv(find_dotenv())

broker = os.getenv("CELERY_BROKER", "redis://localhost:6379/0")
backend = os.getenv("CELERY_BACKEND", "redis://localhost:6379/0")
celery_app = Celery("converter", broker=broker, backend=backend)

celery_app.conf.beat_schedule = {
    "app-schedule": {
        "task": "audio_converter",
        "schedule": timedelta(seconds=5),
        "args": ("Hola Mundo", )
    }
}

@celery_app.task(name="audio_converter")
def audio_converter(message):
    os.system(f"echo {message}")
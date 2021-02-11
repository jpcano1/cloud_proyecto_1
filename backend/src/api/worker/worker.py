from celery import Celery
from dotenv import load_dotenv, find_dotenv
from datetime import timedelta
from flask import Flask

load_dotenv(find_dotenv())

def init_app(app: Flask):
    """
    The app initialization of the celery app
    :param app: The flask app
    :type app: Flask
    :return: the celery app created
    :rtype: Celery
    """
    celery_app = Celery(app.import_name,
                        broker=app.config["CELERY_BROKER"],
                        backend=app.config["CELERY_BACKEND"])
    celery_app.conf.beat_schedule = {
        "app-schedule": {
            "task": "audio_converter",
            "schedule": timedelta(seconds=5)
        }
    }

    TaskBase = celery_app.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app

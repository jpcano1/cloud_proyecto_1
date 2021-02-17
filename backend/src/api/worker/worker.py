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

    # The beat scheduler executes the converter
    # each 15 seconds
    celery_app.conf.beat_schedule = {
        "app-schedule": {
            "task": "audio_converter",
            "schedule": timedelta(seconds=15)
        }
    }

    # The task base app
    TaskBase = celery_app.Task

    # The new task class
    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            """
            When celery calls the task, it will do it
            under a context
            :param args: The function arguments
            :param kwargs: The function keyword arguments
            :return: The task call under the flask app context
            """
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    # We assign the new object
    celery_app.Task = ContextTask
    return celery_app

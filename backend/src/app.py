# App Configurations
from src.api.config import (DevelopmentConfig,
                            ProductionConfig,
                            TestingConfig)

# App Creation
from src.api.utils import create_app, db

from src.api.worker import init_app

# OS Configurations
import os, sys
import logging

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s|%(levelname)s|%(filename)s: %(lineno)s| %(message)s",
    level=logging.DEBUG
)

if os.getenv("WORK_ENV") == "PROD":
    app_config = ProductionConfig
elif os.getenv("WORK_ENV") == "TEST":
    app_config = TestingConfig
else:
    app_config = DevelopmentConfig

app = create_app(app_config)

celery_app = init_app(app)

db.init_app(app)
with app.app_context():
    db.create_all()
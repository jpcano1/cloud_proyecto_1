import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BANNERS_FOLDER = "static/banners"
    CONVERTED_AUDIOS_FOLDER = "static/converted_audios"
    RAW_AUDIOS_FOLDER = "static/raw_audios"
    LOGS_FOLDER = "static/logs"
    PROPAGATE_EXCEPTIONS = True
    CELERY_BROKER = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_BACKEND = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_SCHEDULE_TIME = int(os.getenv("CELERY_SCHEDULE_TIME", 15))

class ProductionConfig(Config):
    POSTGRES_USERNAME = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_DB = os.getenv("POSTGRES_DB")

    SECRET_KEY = os.getenv("SECRET_KEY", None)
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", None)

    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"

    MAIL_DEFAULT_SENDER = os.getenv("EMAIL_SENDER")
    MAIL_SERVER = os.getenv("EMAIL_SERVER")
    MAIL_PORT = os.getenv("EMAIL_PORT")
    MAIL_USERNAME = os.getenv("EMAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    MAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
    MAIL_DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_ECHO = False
    SQLITE_DB = os.getenv("SQLITE_DB", "example.db")

    if os.getenv("ENGINE", "sqlite") == "postgres":
        POSTGRES_USERNAME = os.getenv("POSTGRES_USER")
        POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        POSTGRES_HOST = os.getenv("POSTGRES_HOST")
        POSTGRES_DB = os.getenv("POSTGRES_DB")

        SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"

    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath(SQLITE_DB)

    SECRET_KEY = "cfiG7j1LOu"
    SECURITY_PASSWORD_SALT = "DukVKGDuJk"

    MAIL_DEFAULT_SENDER = os.getenv("EMAIL_SENDER")
    MAIL_SERVER = os.getenv("EMAIL_SERVER")
    MAIL_PORT = os.getenv("EMAIL_PORT")
    MAIL_USERNAME = os.getenv("EMAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    MAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
    MAIL_DEBUG = False

class TestingConfig(Config):
    pass
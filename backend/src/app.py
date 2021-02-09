# Flask Configurations
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# App Configurations
from src.api.config import (DevelopmentConfig,
                            ProductionConfig,
                            TestingConfig)

# Database Configurations
from src.api.utils import db

# OS Configurations
import os, sys
import logging

# Resources
from src.api.views import SignUp, Admin

logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s|%(levelname)s|%(filename)s: %(lineno)s| %(message)s",
    level=logging.DEBUG
)

app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)

if os.getenv("WORK_ENV") == "PROD":
    app_config = ProductionConfig
elif os.getenv("WORK_ENV") == "TEST":
    app_config = TestingConfig
else:
    app_config = DevelopmentConfig

app.config.from_object(app_config)

db.init_app(app)
with app.app_context():
    db.create_all()

api.add_resource(SignUp, "/api/signup")
api.add_resource(Admin, "/api/admin")
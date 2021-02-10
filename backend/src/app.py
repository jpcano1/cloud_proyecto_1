# Flask Configurations
from flask import Flask, send_from_directory
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
from src.api.views import (SignUp, Admin, Contest, VoiceUpload,
                           ContestDetail, Voice, VoiceDetail)

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

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

# Files Creation
@app.route("/uploads/raw_audio/<filename>", methods=["GET"])
def upload_raw_audio(filename):
    """
    Route to upload the raw audio file
    :param filename: The filename of the audio
    :return: The url of the saved audio
    """
    return send_from_directory(app.config["RAW_AUDIOS_FOLDER"], filename)

@app.route("/uploads/converted_audio/<filename>", methods=["GET"])
def upload_converted_audio(filename):
    """
    Route to upload the converted audio file
    :param filename: The filename of the audio
    :return: The url of the saved audio
    """
    return send_from_directory(app.config["CONVERTED_AUDIOS_FOLDER"], filename)

@app.route("/uploads/banner/<filename>", methods=["GET"])
def upload_banner(filename):
    """
    Route to upload the banner file
    :param filename: The filename of the banner
    :return: The url of the saved banner
    """
    return send_from_directory(app.config["BANNERS_FOLDER"], filename)

# Admin Routes
api.add_resource(SignUp, "/api/signup")
api.add_resource(Admin, "/api/admin")

# Contest Routes
api.add_resource(Contest, "/api/contest")
api.add_resource(ContestDetail, "/api/contest/<url>")

# Voice Routes
api.add_resource(Voice, "/api/voice")
api.add_resource(VoiceDetail, "/api/voice/<int:voice_id>")
api.add_resource(VoiceUpload, "/api/voice_upload/<int:voice_id>")
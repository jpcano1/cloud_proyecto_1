# App Configurations
from src.api.config import (DevelopmentConfig,
                            ProductionConfig,
                            TestingConfig)

# Flask Configurations
from flask import send_from_directory, Flask, redirect
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Database Configurations
from src.api.utils import mail

# Resources
from src.api.views import (SignUp, Admin, Contest, VoiceUpload,
                           BannerUpload, Login, ContestDetail,
                           Voice, VoiceDetail, AdminDetail)

from src.api.worker import init_app

# OS Configurations
import os, sys
import logging

import requests

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

def create_app(app_config_):
    app = Flask(__name__)
    app.config.from_object(app_config_)

    if not os.path.exists("src/" + app.config["BANNERS_FOLDER"]):
        os.makedirs("src/" + app.config["BANNERS_FOLDER"])

    if not os.path.exists(os.path.join("src", app.config["CONVERTED_AUDIOS_FOLDER"])):
        os.makedirs(os.path.join("src", app.config["CONVERTED_AUDIOS_FOLDER"]))

    if not os.path.exists(os.path.join("src", app.config["RAW_AUDIOS_FOLDER"])):
        os.makedirs(os.path.join("src", app.config["RAW_AUDIOS_FOLDER"]))

    api = Api(app)
    Bcrypt(app)
    JWTManager(app)
    CORS(app)
    mail.init_app(app)

    @app.route("/src/static/raw_audios/<filename>", methods=["GET"])
    def upload_raw_audio(filename):
        """
        Route to upload the raw audio file
        :param filename: The filename of the audio
        :return: The url of the saved audio
        """
        return redirect(os.getenv("CDN_ADDRESS") + "/src/static/raw_audios/" + filename)

    @app.route("/src/static/converted_audios/<filename>", methods=["GET"])
    def upload_converted_audio(filename):
        """
        Route to upload the converted audio file
        :param filename: The filename of the audio
        :return: The url of the saved audio
        """
        return redirect(os.getenv("CDN_ADDRESS") + "/src/static/converted_audios/" + filename)

    @app.route("/src/static/banners/<filename>", methods=["GET"])
    def upload_banner(filename):
        """
        Route to upload the banner file
        :param filename: The filename of the banner
        :return: The url of the saved banner
        """
        return redirect(os.getenv("CDN_ADDRESS") + "/src/static/banners/" + filename)

    # Admin Routes
    api.add_resource(SignUp, "/api/signup")
    api.add_resource(Login, "/api/login")
    api.add_resource(Admin, "/api/admin")
    api.add_resource(AdminDetail, "/api/admin/<admin_id>")

    # Contest Routes
    api.add_resource(Contest, "/api/contest")
    api.add_resource(ContestDetail, "/api/contest/<url>")
    api.add_resource(BannerUpload, "/api/banner/<contest_url>")

    # Voice Routes
    api.add_resource(Voice, "/api/voice")
    api.add_resource(VoiceDetail, "/api/voice/<voice_id>")
    api.add_resource(VoiceUpload, "/api/voice_upload/<voice_id>")

    return app

app = create_app(app_config)
celery_app = init_app(app)
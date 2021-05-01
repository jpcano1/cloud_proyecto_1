from celery import current_app
from ..controllers import VoiceController
from ..utils import send_email, s3
from flask import render_template
import time
import logging
import os
import requests

from dotenv import  load_dotenv, find_dotenv
load_dotenv(find_dotenv())

voice_controller = VoiceController()

if not os.path.exists("src/static/logs"):
    os.makedirs("src/static/logs")

logger = logging.getLogger("voices_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("src/static/logs/voice.logs")
logger.addHandler(file_handler)

def is_production_environment():
    return current_app.conf.work_env == "PROD"

def get_converted_folder():
    return current_app.conf.converted_audios

def retrieve():
    """
    Retrieves all the non-converted voices
    :return: A collection of voices
    """
    fetched = voice_controller.get_non_converted()

    return fetched

def notify_converted(name, email):
    """
    Creates the notification for the users
    in the platform
    :param name: The name of the user to be notified
    :param email: The email of the user to be notified
    """
    html = render_template(
        "email_templates/notification_email.html",
        name=name
    )
    if is_production_environment():
        send_email(
            to=email,
            subject="Urgent",
            template=html
        )
    print("Email Sent!")

def convert(audio_url):
    """
    This method converts a song from any format to mp3
    :param audio_url: The url of the audio to be converted
    :return: The path of the converted voice
    """
    if audio_url.endswith(".mp3"):
        converted_path = audio_url
    else:
        converted_path = audio_url + ".mp3"

    # Method of conversion
    if not os.path.exists(converted_path):
        os.system(f"ffmpeg -hide_banner -loglevel error -i {audio_url} {converted_path}")
    return converted_path

def download_file(audio_url):
    key = audio_url[1:]
    filename = audio_url.split("/")[-1]
    s3.download_file(
        Bucket=os.getenv("BUCKET_NAME"), Key=key,
        Filename=filename
    )
    converted_path = convert(filename)
    key = "src/" + get_converted_folder() + "/" + converted_path
    s3.upload_file(
        Bucket=os.getenv("BUCKET_NAME"), Key=key,
        Filename=converted_path
    )
    converted_audio = "/src/" + get_converted_folder() + "/" + converted_path
    os.remove(filename)
    os.remove(converted_path)
    return converted_audio

@current_app.task(name="audio_converter")
def converter():
    """
    The converter method, checks the database
    looking for non-converted voices
    """
    fetched_voices = retrieve()

    emails = []

    counter = 0
    init_time = time.time()

    if len(fetched_voices["Items"]) > 0:
        logger.info(f"begin,{init_time}")

        for voice in fetched_voices["Items"]:
            if voice["raw_audio"] != "":
                # Start time
                path = download_file(voice["raw_audio"])
                # Log message
                voice_controller.update(
                    str(voice['id']),
                    value={
                        "converted": True,
                        "converted_audio": path
                    }
                )
                # Update route
                print(f"Voice: {str(voice['id'])} converted")
                emails.append((voice["name"], voice["email"]))
                counter += 1
        end_time = time.time()
        logger.info(f"end,{end_time}")

        requests.post(
            current_app.conf.snitch_url, 
            data={
                "conversion_time": f"Conversion finished in {end_time - init_time}"
            }
        )
        for name, email in emails:
            notify_converted(name, email)
    print(f"Voices converted: {counter}")
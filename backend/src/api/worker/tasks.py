from celery import current_app
from ..models import Voice as VoiceModel
from ..utils import db, send_email
from flask import render_template
import time
import logging
import os

if not os.path.exists("src/static/logs"):
    os.makedirs("src/static/logs")

logger = logging.getLogger("voices_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("src/static/logs/voice.logs")
logger.addHandler(file_handler)

def is_production_environment():
    return current_app.conf.work_env == "PROD"

def retrieve():
    """
    Retrieves all the non-converted voices
    :return: A collection of voices
    """
    fetched = VoiceModel.query.filter_by(
        converted=False
    ).all()

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

def convert(audio_id, audio_url):
    """
    This method converts a song from any format to mp3
    :param audio_id: The id of the audio
    :param audio_url: The url of the audio to be converted
    :return: The path of the converted voice
    """
    # Get the full audio url
    full_path = audio_url[1:]
    # Get the full audio name
    audio_name = full_path.split("/")[-1]
    if audio_name.endswith(".mp3"):
        converted_path = "src/static/converted_audios/" + audio_name
    else:
        converted_path = "src/static/converted_audios/" + audio_name + ".mp3"

    # Method of conversion
    if not os.path.exists(converted_path):
        logger.info(f"{audio_id},begin,{time.time()}")
        os.system(f"ffmpeg -hide_banner -loglevel error -i {full_path} {converted_path}")
        logger.info(f"{audio_id},end,{time.time()}")
    return "/" + converted_path

@current_app.task(name="audio_converter")
def converter():
    """
    The converter method, checks the database
    looking for non-converted voices
    """
    fetched_voices = retrieve()

    emails = []

    counter = 0
    for voice in fetched_voices:
        if voice.raw_audio:
            path = convert(voice.id, voice.raw_audio)
            voice.converted = True
            voice.converted_audio = path
            # Update route
            db.session.add(voice)
            db.session.commit()
            print(f"Voice: {voice.id} converted")
            emails.append((voice.name, voice.email))
            counter += 1

    for name, email in emails:
        notify_converted(name, email)
    print(f"Voices converted: {counter}")
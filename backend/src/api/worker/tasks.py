from celery import current_app
from ..models import Voice as VoiceModel
from ..utils import db, send_email
import os
from flask import render_template

def retrieve():
    fetched = VoiceModel.query.filter_by(
        converted=False
    ).all()

    return fetched

def notify_converted(name, email):
    html = render_template(
        "email_templates/notification_email.html",
        name=name
    )
    send_email(
        to=email,
        subject="Urgent",
        template=html
    )
    print("Email Sent!")

def convert(audio_url):
    full_path = audio_url[1:]
    audio_name = full_path.split("/")[-1]
    if audio_name.endswith(".mp3"):
        converted_path = "src/static/converted_audios/" + audio_name
    else:
        converted_path = "src/static/converted_audios/" + audio_name + ".mp3"

    if not os.path.exists(converted_path):
        print(f"Converting {full_path} to {converted_path}")
        os.system(f"ffmpeg -i {full_path} {converted_path}")
    return "/" + converted_path

@current_app.task(name="audio_converter")
def converter():
    fetched_voices = retrieve()

    counter = 0
    for voice in fetched_voices:
        if voice.audio:
            path = convert(voice.audio)
            voice.converted = True
            voice.audio = path
            db.session.add(voice)
            db.session.commit()
            print(f"Voice: {voice.id} converted")
            notify_converted(voice.name, voice.email)
            counter += 1
    print(f"Voices converted: {counter}")
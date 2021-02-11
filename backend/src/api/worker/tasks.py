from celery import current_app
from ..models import Voice as VoiceModel
from ..utils import db
import os

def retrieve():
    fetched = VoiceModel.query.filter_by(
        converted=False
    ).all()

    return fetched

def convert(audio_url):
    full_path = audio_url[1:]
    audio_name = full_path.split("/")[-1]
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
        path = convert(voice.audio)
        voice.converted = True
        voice.audio = path
        db.session.add(voice)
        db.session.commit()
        print(f"Voice: {voice.id} converted")
        counter += 1
    print(f"Voices converted: {counter}")
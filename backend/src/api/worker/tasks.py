from celery import current_app
from ..models import Voice as VoiceModel, VoiceSchema

def retrieve():
    fetched = VoiceModel.query.filter_by(
        converted=False
    ).all()

    voice_schema = VoiceSchema(many=True)
    voices = voice_schema.dump(fetched)
    return voices

@current_app.task(name="audio_converter")
def converter():
    voices = retrieve()
    print(f"Hay {len(voices)} voces sin convertir")
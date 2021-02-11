from celery import current_app
from ..models import Voice as VoiceModel, VoiceSchema

def retrieve():
    results = VoiceModel.query.filter_by(
        converted=False
    )
    return results

@current_app.task(name="audio_converter")
def converter():
    results = retrieve()
    print(len(results))
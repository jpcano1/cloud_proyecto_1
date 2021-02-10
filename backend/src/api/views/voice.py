from flask_restful import Resource
from flask import request

from ..models import Voice as VoiceModel
from ..models import VoiceSchema
from ..utils import response_with, responses

class Voice(Resource):
    def get(self):
        fetched = VoiceModel.query.all()
        voice_schema = VoiceSchema(many=True)
        voices = voice_schema.dump(fetched)
        return response_with(responses.SUCCESS_200, value={
            "voices": voices
        })

    def post(self):
        data = request.get_json()
        return response_with(responses.SUCCESS_200, value={
            "message": "Voice uploaded!"
        })

class VoiceDetail(Resource):
    pass
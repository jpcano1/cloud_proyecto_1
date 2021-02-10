from flask_restful import Resource
from flask import request, current_app, url_for

from ..models import Voice as VoiceModel
from ..models import VoiceSchema
from ..utils import response_with, responses, db

from marshmallow.exceptions import ValidationError

from werkzeug.utils import secure_filename

import os

allowed_extensions = { ".ogg" }

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
        data["contest"] = 1
        voice_schema = VoiceSchema()
        try:
            voice = voice_schema.load(data, session=db.session)
            voice.create()
        except ValidationError as e:
            a = e.messages.keys()
            return response_with(responses.MISSING_PARAMETERS_422, value={
                "error_message": "Missing Fields: " + ", ".join(a)
            })
        return response_with(responses.SUCCESS_200, value={
            "message": "Voice uploaded!"
        })

class VoiceDetail(Resource):
    def get(self, voice_id):
        fetched = VoiceModel.query.filter_by(
            id=voice_id
        ).first()

        if not fetched:
            return response_with(responses.SERVER_ERROR_404, value={
                "error_message": "Resource does not exist"
            })
        voice_schema = VoiceSchema()
        voice = voice_schema.dump(fetched)
        return response_with(responses.SUCCESS_200, value={
            "voice": voice
        })

    def delete(self, voice_id):
        fetched = VoiceModel.query.filter_by(
            id=voice_id
        ).first()

        if not fetched:
            return response_with(responses.SERVER_ERROR_404, value={
                "error_message": "Resource does not exist"
            })
        db.session.delete(fetched)
        db.session.commit()
        return response_with(responses.SUCCESS_204)

class VoiceUpload(Resource):

    def post(self, voice_id):
        fetched = VoiceModel.query.get_or_404(voice_id)
        file = request.files.get("audio", None)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(
                "src",
                current_app.config["RAW_AUDIOS_FOLDER"],
                filename
            ))
        else:
            return response_with(responses.MISSING_PARAMETERS_422, value={
                "error_message": "There is no file"
            })
        fetched.audio = url_for("upload_raw_audio",
                                filename=filename,
                                _external=True)
        db.session.add(fetched)
        db.session.commit()
        return response_with(responses.SUCCESS_200, value={
            "message": "Audio Uploaded!"
        })
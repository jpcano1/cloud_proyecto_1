# Flask Imports
from flask_restful import Resource
from flask import request, current_app, url_for
import flask_sqlalchemy as fs

# Models and Utils Imports
from ..models import Voice as VoiceModel
from ..models import VoiceSchema
from ..utils import response_with, responses, db

# Marshmallow imports
from marshmallow.exceptions import ValidationError

# Werkzeug utils
from werkzeug.utils import secure_filename
import werkzeug as werk

# OS Imports
import os

from ..controllers import VoiceController

class Voice(Resource):
    @staticmethod
    def paginated_voices(results, pagination: fs.Pagination):
        prev_page = pagination.prev_num
        next_page = pagination.next_num
        value = {
            "voices": results,
            "count": pagination.pages,
            "previous": request.path + f"?page={prev_page}" if prev_page else None,
            "next": request.path + f"?page={next_page}" if next_page else None
        }
        return value

    def get(self):
        """
        Fetches the entire database of voices
        if the voices we're already converted
        :return: A 200 status code message
        """
        page = request.args.get("page", 1, type=int)
        if request.args.get("contest_id"):
            fetched = VoiceModel.query.filter_by(
                contest=request.args.get("contest_id"),
                converted=True
            )
        else:
            fetched = VoiceModel.query.filter_by(
                converted=True
            )

        fetched = fetched.order_by(
            VoiceModel.created.desc()
        ).paginate(
            page=page,
            max_per_page=50
        )

        voice_schema = VoiceSchema(many=True)
        voices = voice_schema.dump(fetched.items)

        value = self.paginated_voices(voices, fetched)

        return response_with(responses.SUCCESS_200,
                             value=value)

    def post(self):
        """
        Creates a voice in the database
        :return: A 200 status code message
        :exception ValidationError: If the
        body request has missing fields.
        """
        data = request.get_json()
        voice_schema = VoiceSchema()

        try:
            voice = voice_schema.load(data, session=db.session)
            result = voice_schema.dump(voice.create())
        except ValidationError as e:
            a = e.messages.keys()
            return response_with(responses.MISSING_PARAMETERS_422, value={
                "error_message": "Missing Fields: " + ", ".join(a)
            })
        return response_with(responses.SUCCESS_200, value={
            "message": "Voice uploaded!",
            "voice": result
        })

class VoiceDetail(Resource):
    def get(self, voice_id):
        """
        Fetches a single voice from the database
        if it was converted
        :param voice_id: The id of the voice
        :return: A 200 status code message
        """
        fetched = VoiceModel.query.filter_by(
            id=voice_id, converted=True
        ).first()
        # If it wasn't found, it returns a 404 status
        # code message.
        if not fetched:
            return response_with(responses.SERVER_ERROR_404, value={
                "error_message": "Resource does not exist or it hasn't been converted"
            })
        voice_schema = VoiceSchema()
        voice = voice_schema.dump(fetched)
        return response_with(responses.SUCCESS_200, value={
            "voice": voice
        })

    def delete(self, voice_id):
        """
        Deletes a voice from the database
        :param voice_id: The id of the voice to be deleted
        :return: A 204 status code message
        """
        # Fetches the voice, if it's not found,
        # it returns a 404 status code message
        fetched = VoiceModel.query.filter_by(
            id=voice_id, converted=True
        ).first()

        if not fetched:
            return response_with(responses.SERVER_ERROR_404, value={
                "error_message": "Resource does not exist"
            })
        db.session.delete(fetched)
        db.session.commit()
        return response_with(responses.SUCCESS_204)

class VoiceUpload(Resource):
    voice_controller = VoiceController()

    def post(self, voice_id):
        """
        Updates the voice to upload the audio file.
        :param voice_id: The id of the existing voice
        :return: A 200 status code message
        """
        fetched = VoiceModel.query.get_or_404(voice_id)
        # This is the file from the form-data
        file: werk.FileStorage = request.files.get("audio", None)
        # If it was submitted, save it
        if fetched:
            # Controller stage of the voice file
            if not self.voice_controller(file.content_type):
                return response_with(responses.INVALID_INPUT_422,
                                     error="File type not allowed")
            if file and self.voice_controller(file.content_type):
                filename = secure_filename("_".join([
                    str(fetched.id), fetched.name,
                    fetched.last_name, file.filename
                ]))
                # Saves it in the directory
                file.save(os.path.join(
                    "src",
                    current_app.config["RAW_AUDIOS_FOLDER"],
                    filename
                ))
            else:
                return response_with(responses.MISSING_PARAMETERS_422, value={
                    "error_message": "There is no file"
                })
            # To the saved audio, defines the url to find it
            # the url is defined w.r.t the function defined
            # in the app.py
            fetched.audio = url_for("upload_raw_audio",
                                    filename=filename,
                                    _external=False)
            db.session.add(fetched)
            db.session.commit()
            return response_with(responses.SUCCESS_200, value={
                "message": "Audio Uploaded!"
            })

        return response_with(responses.SERVER_ERROR_404)
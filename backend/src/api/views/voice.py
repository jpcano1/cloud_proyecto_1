# Flask Imports
from flask_restful import Resource
from flask import request, current_app
from flask_jwt_extended import jwt_required

# Models and Utils Imports
from ..models import VoiceModel
from ..utils import response_with, responses, db

# Werkzeug utils
from werkzeug.utils import secure_filename
import werkzeug as werk

# OS Imports
import os
import pymongo

from ..controllers import VoiceController

class Voice(Resource):
    voice_controller = VoiceController()

    @staticmethod
    def paginated_voices(results: pymongo.cursor.Cursor, page_num):
        """
        This methods paginates the voices list
        :param results: The results from the queried voices
        :param pagination: The pagination object in charge of
        manage the pagination
        :type pagination: fs.Pagination
        :return: The response body
        """
        skips = 50 * (page_num - 1)
        # value = {
        #     "count": results.,
        #     "previous": request.path + f"?page={prev_page}" if prev_page else None,
        #     "next": request.path + f"?page={next_page}" if next_page else None,
        #     "voices": results,
        # }
        return {}

    def get(self):
        """
        Fetches the entire database of voices
        if the voices we're already converted
        :return: A 200 status code message
        """
        contest_id = request.args.get("contest_id", None)
        result = self.voice_controller.list(contest_id)

        # value = self.paginated_voices(voices, fetched)

        return response_with(responses.SUCCESS_200,
                             value={
                                 "voices": result
                             })

    def post(self):
        """
        Creates a voice in the database
        :exception ValidationError: If the
        body request has missing fields.
        :return: A 200 status code message
        """
        data = request.get_json()
        result = self.voice_controller.post(data)
        return response_with(responses.SUCCESS_200, value={
            "message": "Voice uploaded!",
            "voice": result.inserted_id
        })

class VoiceDetail(Resource):
    voice_controller = VoiceController()

    def get(self, voice_id):
        """
        Fetches a single voice from the database
        if it was converted
        :param voice_id: The id of the voice
        :return: A 200 status code message
        """
        try:
            voice = self.voice_controller.get(voice_id)
            return response_with(responses.SUCCESS_200, value={
                "voice": voice
            })
        except ValueError as e:
            return response_with(responses.SERVER_ERROR_404,
                                 error=e)

    # @jwt_required()
    # def delete(self, voice_id):
    #     """
    #     Deletes a voice from the database
    #     :param voice_id: The id of the voice to be deleted
    #     :return: A 204 status code message
    #     """
    #     # Fetches the voice, if it's not found,
    #     # it returns a 404 status code message
    #     fetched: VoiceModel = VoiceModel.query.get_or_404(voice_id)
    #
    #     if not fetched:
    #         return response_with(responses.SERVER_ERROR_404, value={
    #             "error_message": "Resource does not exist"
    #         })
    #
    #     # Deletes the raw audio
    #     if fetched.raw_audio != "" and os.path.exists(fetched.raw_audio[1:]):
    #         os.remove(fetched.raw_audio[1:])
    #
    #     # Deletes converted audio
    #     if (fetched.converted and fetched.converted_audio != ""
    #             and os.path.exists(fetched.converted_audio[1:])):
    #         os.remove(fetched.converted_audio[1:])
    #
    #     db.session.delete(fetched)
    #     db.session.commit()
    #     return response_with(responses.SUCCESS_204)

class VoiceUpload(Resource):
    voice_controller = VoiceController()

    def post(self, voice_id):
        """
        Updates the voice to upload the audio file.
        :param voice_id: The id of the existing voice
        :return: A 200 status code message
        """
        try:
            fetched = self.voice_controller.get(voice_id)
            file: werk.FileStorage = request.files.get("audio", None)
            if fetched.get("raw_audio", "") == "":
                if file and not self.voice_controller.validate_format(file.content_type):
                    return response_with(responses.INVALID_INPUT_422,
                                         error="File type not allowed")
                elif file and self.voice_controller.validate_format(file.content_type):
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

                raw_audio = os.path.join(
                    "/src",
                    current_app.config["RAW_AUDIOS_FOLDER"],
                    filename
                )
                self.voice_controller.update(
                    _id=voice_id,
                    value={
                        "raw_audio": raw_audio
                    }
                )
                return response_with(responses.SUCCESS_200, value={
                    "message": "Audio Uploaded!"
                })

            return response_with(responses.FORBIDDEN_403,
                          error="Voice already has audio file")
        except ValueError as e:
            return response_with(responses.SERVER_ERROR_404,
                                 error=e)
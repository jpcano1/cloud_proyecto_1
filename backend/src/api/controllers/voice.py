from ..models import VoiceModel
from datetime import datetime

allowed_extensions = {
    "audio/ogg", "audio/wave",
    "audio/x-flac", "audio/mp4",
    "audio/x-aac", "audio/x-ms-wma",
    "audio/mpeg",
}

class VoiceController:
    def __init__(self):
        self.voice_model = VoiceModel()

    def get(self, _id):
        return self.voice_model.find_one(_id)

    def list(self, contest_id):
        return self.voice_model.find(contest_id)

    def post(self, value: dict):
        value["created"] = datetime.now()
        return self.voice_model.create(value)

    @staticmethod
    def validate_format(format_):
        """
        Function to validate a sound format
        :param format_: The format from parameter
        :return: The format validated if it belongs
        to the allowed file types
        :rtype: bool
        """
        return format_ in allowed_extensions

    def __call__(self, *args, **kwargs):
        """
        This function is called when the VoiceController
        object is called
        :param args: The function arguments
        :param kwargs: The function keyword arguments
        :return: The result of the validation
        """
        return self.validate_format(*args)
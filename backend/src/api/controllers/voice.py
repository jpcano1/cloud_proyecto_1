from ..models import VoiceModel

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
        result =  self.voice_model.find_one(_id)
        if not result:
            raise ValueError("Resource not found")
        return  result

    def list(self, contest_id):
        return self.voice_model.find(contest_id)

    def post(self, value: dict):
        return self.voice_model.create(value)

    def update(self, _id, value):
        return self.voice_model.update(
            _id=_id,
            value=value
        )

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
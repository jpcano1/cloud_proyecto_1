from ..models import VoiceModel, ContestModel
from bson import ObjectId

allowed_extensions = {
    "audio/ogg", "audio/wave",
    "audio/x-flac", "audio/mp4",
    "audio/x-aac", "audio/x-ms-wma",
    "audio/mpeg", "audio/wav",
}

class VoiceController:
    def __init__(self):
        self.voice_model = VoiceModel()
        self.contest_model = ContestModel()

    def get(self, _id):
        result =  self.voice_model.find_one(_id)
        if not result:
            raise ValueError("Resource not found")
        return self.voice_model.to_dict(result)

    def get_non_converted(self):
        return self.voice_model.find_non_converted()

    def list(self, contest_id):
        return [self.voice_model.to_dict(x) for x in self.voice_model.find(contest_id)]

    def post(self, value: dict):
        result = self.contest_model.find_one(value["contest_url"])
        if not result:
            raise ValueError("Contest doesn't exist")
        return self.voice_model.create(value)

    def update(self, _id, value):
        result = self.voice_model.update(
            _id=_id,
            value=value
        )
        if result.matched_count < 1:
            raise ValueError("Resource does not exist")

    def delete(self, _id):
        result = self.voice_model.delete(_id)
        if result.deleted_count < 1:
            raise ValueError("Resource does not exist")

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
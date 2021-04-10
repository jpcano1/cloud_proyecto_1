from ..utils import db
from pymongo.collection import Collection

class VoiceModel:
    voices: Collection = db.db.voices
    def create(self, value: dict):
        """
        Creates the voice in the database
        :return: The voice created
        """
        return self.voices.insert_one(value)

    def find(self, contest_id):
        return self.voices.find({
            "contest_id": contest_id
        })

    def update(self, _id, contest_id, value):
        return self.voices.update_one(
            {
                "_id": _id,
                "contest_id": contest_id
            },
            value
        )
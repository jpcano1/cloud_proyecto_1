import pymongo
from datetime import datetime

from ..utils import db
from pymongo.collection import Collection

class VoiceModel:
    voices: Collection = db.db.voices
    def create(self, value: dict):
        """
        Creates the voice in the database
        :return: The voice created
        """
        value["created"] = datetime.now()
        return self.voices.insert_one(value)

    def find(self, contest_id):
        if contest_id:
            result = self.voices.find({
                "contest_id": contest_id
            })
        else:
            result = self.voices.find({})
        return result.sort(
            "created",
            pymongo.DESCENDING
        )

    def find_one(self, _id):
        return self.voices.find_one({
            "_id": _id
        })

    def update(self, _id, contest_id, value: dict):
        return self.voices.update_one(
            {
                "_id": _id,
                "contest_id": contest_id
            },
            value
        )
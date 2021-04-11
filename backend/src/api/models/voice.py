import pymongo
from datetime import datetime

from ..utils import db
from pymongo.collection import Collection
from bson import ObjectId

class VoiceModel:
    voices: Collection = db.voices

    def create(self, value: dict):
        """
        Creates the voice in the database
        :return: The voice created
        """
        value["created"] = datetime.now()
        value["converted"] = False
        value["raw_audio"] = ""
        value["converted_audio"] = ""
        return self.voices.insert_one(value)

    def find(self, contest_url):
        if contest_url:
            result = self.voices.find({
                "contest_url": contest_url
            })
        else:
            result = self.voices.find({})
        return result.sort(
            "created",
            pymongo.DESCENDING
        )

    def find_one(self, _id):
        return self.voices.find_one({
            "_id": ObjectId(_id)
        })

    def find_non_converted(self):
        return self.voices.find({
            "converted": False
        })

    def update(self, _id, value: dict):
        return self.voices.update_one(
            {"_id": ObjectId(_id)},
            {"$set": value}
        )

    def delete(self, _id):
        return self.voices.delete_one(
            {"_id": ObjectId(_id)}
        )

    @staticmethod
    def to_dict(mongo_object):
        mongo_object["_id"] = str(mongo_object["_id"])
        mongo_object["created"] = str(mongo_object["created"])
        return mongo_object
from ..utils import db
from pymongo.collection import Collection

class ContestModel:
    contests: Collection = db.db.contests

    def create(self, value: dict):
        """
        Creates the contest in the database
        :return: The contest created
        """
        return self.contests.insert_one(value)

    def find(self, admin_id):
        if admin_id:
            return self.contests.find({
                "admin_id": admin_id
            })
        return self.contests.find({})

    def find_one(self, url):
        return self.contests.find_one({
            "url": url,
        })

    def update(self, url, admin_id, value):
        return self.contests.update_one(
            {
                "admin_id": admin_id,
                "url": url
            },
            value
        )

    def delete(self, url, admin_id):
        return self.contests.delete_one(
            {
                "admin_id": admin_id,
                "url": url
            }
        )

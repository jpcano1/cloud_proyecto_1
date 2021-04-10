from ..utils import db
from .contest import ContestSchema

# Database and Schema Modeling
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from pymongo.collection import Collection

# Encryption Libraries
from flask_bcrypt import generate_password_hash, check_password_hash

class AdminModel:
    admins: Collection = db.db.admins

    def create(self, value: dict):
        """
        Creates the admin in the database
        :return: The admin created
        """
        return self.admins.insert_one(value)

    def find_one(self, _id):
        return self.admins.find_one(
            {"_id": _id}
        )

    def find(self):
        return self.admins.find({})

    def update(self, _id, value: dict):
        return self.admins.update_one(
            {"_id": _id},
            value
        )

    def find_by_email(self, email):
        """
        Finds admin user by email in the database
        :param email: The email of the user to be found
        :param password: The password of the user to be
        authenticated
        :return: The user found, else None
        """
        return self.admins.find_one({
            "email": email
        })

    @staticmethod
    def generate_hash(password):
        """
        Generates the hash for the password in order
        to encrypt the password in the database
        :param password: The password to be hashed
        :return: The hash of the encrypted password
        """
        return generate_password_hash(password).decode("utf-8")

    @staticmethod
    def verify_hash(hash_, password):
        """
        Verifies the hash from the password in the
        database with the password coming from login
        :param hash_: The hashed password in the database
        :param password: The password to be verified
        :return: The verification, True if correct,
        False if incorrect
        :rtype: bool
        """
        return check_password_hash(hash_, password)
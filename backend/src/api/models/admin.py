from ..utils import db
from .contest import ContestSchema

# Database and Schema Modeling
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

# Encryption Libraries
from flask_bcrypt import generate_password_hash, check_password_hash

class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    contests = db.relationship("Contest", backref="Admin", cascade="all, delete-orphan")

    def __init__(self, name, last_name, email, password):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.password = password

    def create(self):
        """
        Creates the admin in the database
        :return: The admin created
        """
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_by_email(cls, email):
        """
        Finds admin user by email in the database
        :param email: The email of the user to be found
        :return: The user found, else None
        """
        return cls.query.filter_by(email=email).first()

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

class AdminSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Admin
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(load_only=True, required=True)
    contests = fields.Nested(
        ContestSchema,
        many=True,
        only=[
            "id",
            "name",
            "prize",
            "banner"
        ]
    )
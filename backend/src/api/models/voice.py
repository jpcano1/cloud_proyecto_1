from ..utils import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

class Voice(db.Model):
    __tablename__ = "voices"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    audio = db.Column(db.String(20), default="")
    observations = db.Column(db.String(120), default="")
    converted = db.Column(db.Boolean, nullable=False, default=False)
    contest = db.Column(db.Integer, db.ForeignKey("contests.id"))

class VoiceSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Voice
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    name = fields.String()
    last_name = fields.String()
    email = fields.Email(required=True)
    audio = fields.String(dump_only=True)
    observations = fields.String()
    contest = fields.Integer(required=True)
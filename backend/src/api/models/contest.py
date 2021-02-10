from ..utils import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

from .voice import VoiceSchema

class Contest(db.Model):
    __tablename__ = "contests"
    __table_args__ = (
        db.CheckConstraint("end_date > begin_date"),
        db.CheckConstraint("prize > 0.0"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    banner = db.Column(db.String(20), default="")
    url = db.Column(db.String(50), nullable=False, unique=True)
    begin_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    prize = db.Column(db.Float, nullable=False)
    script = db.Column(db.String(120), nullable=False)
    recommendations = db.Column(db.String(120), default="")
    admin = db.Column(db.Integer, db.ForeignKey("admins.id"))
    voices = db.relationship("Voice", backref="Contest", cascade="all, delete-orphan")

class ContestSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Contest
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    banner = fields.String(dump_only=True)
    url = fields.String(required=True)
    begin_date = fields.DateTime(format="%d/%m/%Y", required=True)
    end_date = fields.DateTime(format="%d/%m/%Y", required=True)
    prize = fields.Float(required=True)
    script = fields.String(required=True)
    recommendations = fields.String()
    admin = fields.Integer(required=True)
    voices = fields.Nested(
        VoiceSchema,
        many=True,
        only=["id", "email"]
    )
from ..utils import db
from marshmallow_sqlalchemy import ModelSchema

class Voice(db.Model):
    pass

class VoiceSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Voice
        sqla_session = db.session
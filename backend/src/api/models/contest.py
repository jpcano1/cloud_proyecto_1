from ..utils import db
from marshmallow_sqlalchemy import ModelSchema

class Contest(db.Model):
    pass

class ContestSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Contest
        sqla_session = db.session
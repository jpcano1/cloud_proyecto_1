from ..utils import db
from marshmallow_sqlalchemy import ModelSchema

class Admin(db.Model):
    pass

class AdminSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Admin
        sqla_session = db.session
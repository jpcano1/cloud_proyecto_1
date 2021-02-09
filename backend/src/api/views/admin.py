from flask_restful import Resource
from flask import request
from ..utils import db, responses, response_with
from ..models import Admin as AdminModel
from ..models import AdminSchema
from sqlalchemy.exc import IntegrityError

class SignUp(Resource):
    def post(self):
        """
        Creates an admin to the database
        :return: a HTTP response with a status code 200
        :exception IntegrityError: Returns a 422 status code
        response if the email already exists
        :exception KeyError: Returns a 422 status code
        response if the body of the request doesn't have
        all the parameters
        """
        data = request.get_json()
        if (not data.get("password") or not data.get("email")
            or not data.get("name") or not data.get("last_name")):
            return response_with(responses.MISSING_PARAMETERS_422)
        data["password"] = AdminModel.generate_hash(data["password"])
        admin_schema = AdminSchema()
        admin = admin_schema.load(data, session=db.session)

        try:
            admin.create()
        except IntegrityError:
            return response_with(responses.INVALID_FIELD_NAME_SENT_422, value={
                "error_message": "Email already exists"
            })
        except Exception as e:
            return response_with(responses.INVALID_INPUT_422, value={
                "error_message": str(e)
            })
        return response_with(responses.SUCCESS_200, value={
            "message": "Admin created"
        })

class Admin(Resource):
    def get(self):
        """
        Retrieves all the admins of the database
        (will be deleted)
        :return: All the admins in the database
        """
        fetched = AdminModel.query.all()
        admin_schema = AdminSchema(many=True)
        admins = admin_schema.dump(fetched)
        return response_with(responses.SUCCESS_200, value={
            "admins": admins
        })
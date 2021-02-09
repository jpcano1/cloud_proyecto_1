from flask_restful import Resource
from flask import request
from ..utils import db, responses, response_with
from ..models import Admin as AdminModel
from ..models import AdminSchema
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from flask_jwt_extended import create_access_token

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

class Login(Resource):
    def post(self):
        """
        Submits an admin info to login
        :return: The logged on admin user.
        """
        data = request.get_json()
        current_user = AdminModel.find_by_email(data["email"])

        if not current_user:
            return response_with(responses.INVALID_FIELD_NAME_SENT_422, value={
                "error_message": "Wrong email or password"
            })
        verification = AdminModel.verify_hash(current_user.password,
                                              data["password"])
        if not verification:
            return response_with(responses.INVALID_FIELD_NAME_SENT_422, value={
                "error_message": "Wrong email or password"
            })
        expires = timedelta(hours=2)
        access_token = create_access_token(
            identity=str(current_user.id),
            expires_delta=expires
        )
        return response_with(responses.SUCCESS_200, value={
            "access_token": access_token,
            "message": f"Logged in as {current_user.name}"
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
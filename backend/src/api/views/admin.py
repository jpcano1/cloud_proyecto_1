from flask_restful import Resource
from flask import request
from ..utils import db, responses, response_with
from ..models import Admin as AdminModel
from ..models import AdminSchema
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from flask_jwt_extended import create_access_token
from marshmallow.exceptions import ValidationError

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
        :exception ValidationError: Returns a 422 because of
        missing fields
        """
        data = request.get_json()
        admin_schema = AdminSchema()
        try:
            data["password"] = AdminModel.generate_hash(data["password"])
            admin = admin_schema.load(data, session=db.session)
            admin.create()

        # The user already exists
        except IntegrityError:
            return response_with(responses.INVALID_FIELD_NAME_SENT_422, value={
                "error_message": "Email already exists"
            })
        # The body is incomplete
        except KeyError:
            return response_with(responses.MISSING_PARAMETERS_422,
                                 error="Missing Fields: password")
        # Missing fields
        except ValidationError as e:
            a = e.messages.keys()
            return response_with(responses.MISSING_PARAMETERS_422,
                                 error="Missing Fields: " + ", ".join(a))
        # General exception
        except Exception as e:
            return response_with(responses.INVALID_INPUT_422, error=str(e))

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
        current_user = AdminModel.find_by_email(data.get("email"))

        if not current_user:
            return response_with(responses.INVALID_FIELD_NAME_SENT_422,
                                 error="Wrong email or password")
        verification = AdminModel.verify_hash(current_user.password,
                                              data["password"])
        if not verification:
            return response_with(responses.INVALID_FIELD_NAME_SENT_422,
                                 error="Wrong email or password")
        # JWT with 2 hours validity
        expires = timedelta(hours=2)
        access_token = create_access_token(
            identity=str(current_user.id),
            expires_delta=expires
        )
        return response_with(responses.SUCCESS_200, value={
            "admin_id": current_user.id,
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

class AdminDetail(Resource):
    def get(self, admin_id):
        """
        Retrieves the list of admins
        :param admin_id: The id of the admin to retrieve
        :return: The admin retrieved
        """
        fetched = AdminModel.query.get_or_404(admin_id)
        admin_schema = AdminSchema()
        admin = admin_schema.dump(fetched)
        return response_with(responses.SUCCESS_200, value={
            "admin": admin
        })
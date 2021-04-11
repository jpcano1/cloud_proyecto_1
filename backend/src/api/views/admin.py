from flask_restful import Resource
from flask import request
from ..utils import responses, response_with
from ..controllers import AdminController
from bson.json_util import dumps

class SignUp(Resource):
    admin_controller = AdminController()

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
        try:
            result = self.admin_controller.signup(data)

        # The user already exists
        except ValueError as e:
            return response_with(responses.INVALID_FIELD_NAME_SENT_422,
                                 error=str(e))
        # The body is incomplete
        except KeyError:
            return response_with(responses.MISSING_PARAMETERS_422,
                                 error="Missing Fields")
        # General exception
        except Exception as e:
            return response_with(responses.INVALID_INPUT_422, error=str(e))
        return response_with(responses.SUCCESS_201, value={
            "message": "Admin created",
            "_id": str(result.inserted_id)
        })

class Login(Resource):
    admin_controller = AdminController()

    def post(self):
        """
        Submits an admin info to login
        :return: The logged on admin user.
        """
        data = request.get_json()

        try:
            current_user = self.admin_controller.login(data)
        except ValueError as e:
            return response_with(responses.INVALID_FIELD_NAME_SENT_422,
                                 error=e)
        # user_agent = request.user_agent

        # if current_app.config["WORK_ENV"] == "PROD":
        #     template = render_template(
        #         "email_templates/login_email.html",
        #         platform=user_agent.platform,
        #         browser=user_agent.browser,
        #         time=datetime.now()
        #     )
        #
        #     send_email(data.get("email"), "Login Notification", template)
        return response_with(responses.SUCCESS_200, value={
            "admin_id": current_user["admin_id"],
            "access_token": current_user["access_token"],
        })

class Admin(Resource):
    admin_controller = AdminController()

    def get(self):
        """
        Retrieves all the admins of the database
        (will be deleted)
        :return: All the admins in the database
        """
        fetched = self.admin_controller.list()
        return response_with(responses.SUCCESS_200, value={
            "admins": fetched
        })

class AdminDetail(Resource):
    admin_controller = AdminController()

    def get(self, admin_id):
        """
        Retrieves the list of admins
        :param admin_id: The id of the admin to retrieve
        :return: The admin retrieved
        """
        try:
            fetched_admin = self.admin_controller.get(admin_id)
        except ValueError as e:
            return response_with(responses.SERVER_ERROR_404,
                                 error=str(e))

        return response_with(responses.SUCCESS_200, value={
            "admin": fetched_admin
        })
# Flask Libraries
from flask_restful import Resource
from flask import request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

# Werkzeug utils
from werkzeug.utils import secure_filename
import werkzeug as werk

# Util Imports
from ..utils import responses, db, response_with

#os
import os

#AWS SDK
import boto3

#Creating connection to s3 Client
s3 = boto3.client('s3',
                  aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                  aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
                  )
BUCKET_NAME = os.getenv("BUCKET_NAME")

# Models Imports
from ..models import ContestModel

from datetime import datetime as dt


from ..controllers import ContestController

class Contest(Resource):
    contest_controller = ContestController()

    def get(self):
        """
        Retrieves the list con contest in the entire
        database
        :return: The list of contests
        """
        # If the query param admin exists, it filters
        # otherwise, it returns everything
        admin_id = request.args.get("admin_id", None)
        contest_list = self.contest_controller.list(admin_id)
        return response_with(responses.SUCCESS_200, value={
            "contests": contest_list
        })

    @jwt_required()
    def post(self):
        """
        Creates a contest in the database
        :exception ValidationError: If the body request
        has missing fields
        :exception IntegrityError: If the url already exists
        in the database or if the user doesn't
        :exception Exception: If there another error during
        the execution
        :return: A 200 status code message
        """

        # The body data
        data = request.get_json()
        # The identity of the creator admin
        data["admin_id"] = get_jwt_identity()

        try:
            contest_created = self.contest_controller.post(data)
            return response_with(responses.SUCCESS_200, value={
                "message": "Contest created",
                "contest": str(contest_created.inserted_id)
            })
        except ValueError as e:
            return response_with(responses.INVALID_FIELD_NAME_SENT_422,
                                 error=str(e))

class ContestDetail(Resource):
    contest_controller = ContestController()

    def get(self, url):
        """
        Retrieves a contest from its url
        :param url: The url to filter the contest
        :return: A 200 status code message if the contest
        was found, otherwise, 404 error
        """
        try:
            fetched = self.contest_controller.get(url)
        except ValueError as e:
            return response_with(responses.SERVER_ERROR_404,
                                 error=str(e))
        return response_with(responses.SUCCESS_200, value={
            "contest": fetched
        })

    @jwt_required()
    def put(self, url):
        """
        Updates a contest in the database
        :param url: The url of the contest to be retrieved
        :return: A 200 status code answer if updated, otherwise
        a 404 error if not found
        """
        # Identity of the updater admin
        admin_id = get_jwt_identity()
        data = request.get_json()
        try:
            self.contest_controller.update(
                url=url,
                admin_id=admin_id,
                data=data
            )
        except ValueError as e:
            return response_with(responses.SERVER_ERROR_404,
                                 error=str(e))
        return response_with(responses.SUCCESS_200, value={
            "message": "Contest updated"
        })

    @jwt_required()
    def delete(self, url):
        """
        Deletes a contest from the database
        :param url: The url of the contest to be deleted
        :return: A 204 status code message if deleted, otherwise
        a 404 status code response if not found
        """
        # The identity of the deleter admin
        admin_id = get_jwt_identity()
        try:
            self.contest_controller.delete(
                url=url,
                admin_id=admin_id
            )
        except ValueError as e:
            return response_with(responses.SERVER_ERROR_404,
                                 error=str(e))
        return response_with(responses.SUCCESS_204)

class BannerUpload(Resource):
    contest_controller = ContestController()

    @jwt_required()
    def post(self, contest_url):
        """
        Updates the banner of the contest
        :param contest_url: The url of the existing contest
        :return: A 200 status code message if updated, otherwise,
        a 404 error if not found.
        """
        # The id of the updater admin
        admin_id = get_jwt_identity()
        try:
            self.contest_controller.get(contest_url)
            # The storage process from the banner in the form-data
            # body request
            file: werk.FileStorage = request.files.get("banner", None)

            # Validate the file type with the controller
            if file and not self.contest_controller.validate_format(file.content_type):
                return response_with(responses.INVALID_INPUT_422,
                                     error="File type not allowed")
            elif file and self.contest_controller.validate_format(file.content_type):
                filename = secure_filename("_".join([
                    contest_url,
                    file.filename
                ]))
                file.save(
                    filename
                )

            else:
                return response_with(responses.INVALID_INPUT_422,
                                     error="There is no file")
            #Create a url to store in the Bucket
            key = "src/" +  current_app.config["BANNERS_FOLDER"] + "/" + filename

            # Create a url to the image
            banner = "/src/" + current_app.config["BANNERS_FOLDER"] + "/" + filename

            #Upload the file to the bucket
            s3.upload_file(Bucket = BUCKET_NAME, Key=key, Filename= filename)

            #Delete the file once is uploaded
            os.remove(filename)

            self.contest_controller.update(
                url=contest_url,
                admin_id=admin_id,
                data={
                    "banner": banner
                }
            )
            return response_with(responses.SUCCESS_200, value={
                "message": "File Uploaded!"
            })
        except ValueError as e:
            return response_with(responses.SERVER_ERROR_404,
                                 error=str(e))
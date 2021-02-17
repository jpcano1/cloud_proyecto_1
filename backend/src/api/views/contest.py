# Flask Libraries
from flask_restful import Resource
from flask import request, current_app, url_for
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity

# Werkzeug utils
from werkzeug.utils import secure_filename
import werkzeug as werk

# Util Imports
from ..utils import responses, db, response_with

# Marshmallow Imports
from marshmallow.exceptions import ValidationError

# Models Imports
from ..models import Contest as ContestModel, ContestSchema

from datetime import datetime as dt
import os

from ..controllers import ContestController

class Contest(Resource):
    def get(self):
        """
        Retrieves the list con contest in the entire
        database
        :return: The list of contests
        """

        # If the query param admin exists, it filters
        # otherwise, it returns everything
        if request.args.get("admin_id"):
            fetched = ContestModel.query.filter_by(
                admin=request.args.get("admin_id")
            ).all()
        else:
            fetched = ContestModel.query.all()
        contest_schema = ContestSchema(many=True)
        contests = contest_schema.dump(fetched)
        return response_with(responses.SUCCESS_200, value={
            "contests": contests
        })

    @jwt_required()
    def post(self):
        """
        Creates a contest in the database
        :exception ValidationError: If the body request
        has missing fields
        :exception IntegrityError: If the url already exists
        in the database
        :exception Exception: If there another error during
        the execution
        :return: A 200 status code message
        """

        # The body data
        data = request.get_json()
        # The identity of the creator admin
        data["admin"] = get_jwt_identity()
        contest_schema = ContestSchema()

        try:
            contest = contest_schema.load(data, session=db.session)
            result = contest_schema.dump(contest.create())
        except ValidationError as e:
            a = e.messages.keys()
            return response_with(responses.MISSING_PARAMETERS_422,
                                 error="Missing Fields: " + ", ".join(a))
        except IntegrityError:
            return response_with(responses.INVALID_FIELD_NAME_SENT_422,
                                 error="Url already exists")
        except Exception as e:
            return response_with(responses.INVALID_INPUT_422,
                                 error=str(e))
        return response_with(responses.SUCCESS_200, value={
            "message": "Contest created",
            "contest": result
        })

class ContestDetail(Resource):
    def get(self, url):
        """
        Retrieves a contest from its url
        :param url: The url to filter the contest
        :return: A 200 status code message if the contest
        was found, otherwise, 404 error
        """
        fetched = ContestModel.query.filter_by(
            url=url
        ).first()
        if not fetched:
            return response_with(responses.SERVER_ERROR_404,
                                 error="Resource does not exists")
        contest_schema = ContestSchema()
        contest = contest_schema.dump(fetched)
        return response_with(responses.SUCCESS_200, value={
            "contest": contest
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
        contest = ContestModel.query.filter_by(
            url=url, admin=admin_id
        ).first()
        if not contest:
            return response_with(responses.SERVER_ERROR_404,
                                 error="Resource does not exists")

        # Looks every field in the request body
        data = request.get_json()
        if "name" in data:
            contest.name = data["name"]
        if "banner" in data:
            contest.banner = data["banner"]
        if "url" in data:
            contest.url = data["url"]
        if "begin_date" in data:
            contest.begin_date = dt.strptime(data["begin_date"], "%d/%m/%Y")
        if "end_date" in data:
            contest.end_date = dt.strptime(data["end_date"], "%d/%m/%Y")
        if "prize" in data:
            contest.prize = data["prize"]
        if "script" in data:
            contest.script = data["script"]
        if "recommendations" in data:
            contest.recommendations = data["recommendations"]

        db.session.add(contest)
        db.session.commit()
        contest_schema = ContestSchema()
        contest = contest_schema.dump(contest)
        return response_with(responses.SUCCESS_200, value={
            "event": contest
        })

    @jwt_required()
    def delete(self, url):
        """
        Deletes a contest from the database
        :param url: The url of the contest to be deleted
        :return: A 204 status code message
        """
        admin_id = get_jwt_identity()
        fetched = ContestModel.query.filter_by(
            url=url, admin=admin_id
        ).first()
        if not fetched:
            return response_with(responses.SERVER_ERROR_404,
                                 error="Resource does not exists")
        db.session.delete(fetched)
        db.session.commit()
        return response_with(responses.SUCCESS_204)

class BannerUpload(Resource):
    contest_controller = ContestController()

    @jwt_required()
    def post(self, contest_id):
        """

        :param contest_id:
        :type contest_id:
        :return:
        :rtype:
        """
        admin_id = get_jwt_identity()
        fetched = ContestModel.query.filter_by(
            admin=admin_id, id=contest_id
        ).first()
        if fetched:
            file: werk.FileStorage = request.files.get("banner", None)
            if file and not self.contest_controller(file.content_type):
                return response_with(responses.INVALID_INPUT_422,
                                     error="File type not allowed")
            elif file and self.contest_controller(file.content_type):
                filename = secure_filename("_".join([
                    fetched.url,
                    file.filename
                ]))
                file.save(os.path.join(
                    "src",
                    current_app.config["BANNERS_FOLDER"],
                    filename
                ))
            else:
                return response_with(responses.INVALID_INPUT_422,
                                     error="There is no file")
            fetched.banner = url_for("upload_banner",
                                     filename=filename)
            db.session.add(fetched)
            db.session.commit()
            return response_with(responses.SUCCESS_200, value={
                "message": "File Uploaded!"
            })
        return response_with(responses.SERVER_ERROR_404)
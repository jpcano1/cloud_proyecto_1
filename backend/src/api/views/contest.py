# Flask Libraries
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity

# Util Imports
from ..utils import responses, db, response_with

# Marshmallow Imports
from marshmallow.exceptions import ValidationError

# Models Imports
from ..models import Contest as ContestModel, ContestSchema

from datetime import datetime as dt

class Contest(Resource):
    def get(self):
        contests = ContestModel.query.all()
        contest_schema = ContestSchema(many=True)
        contests = contest_schema.dump(contests)
        return response_with(responses.SUCCESS_200, value={
            "contests": contests
        })

    @jwt_required
    def post(self):
        data = request.get_json()
        data["admin"] = get_jwt_identity()
        contest_schema = ContestSchema()

        try:
            contest = contest_schema.load(data, session=db.session)
            contest.create()
        except ValidationError as e:
            a = e.messages.keys()
            return response_with(responses.MISSING_PARAMETERS_422, value={
                "error_message": "Missing Fields: " + ", ".join(a)
            })
        except IntegrityError:
            return response_with(responses.INVALID_FIELD_NAME_SENT_422, value={
                "error_message": "Url already exists"
            })
        except Exception as e:
            return response_with(responses.INVALID_INPUT_422, value={
                "error_message": str(e)
            })
        return response_with(responses.SUCCESS_200, value={
            "message": "Contest created",
        })

class ContestDetail(Resource):
    def get(self, url):
        contest = ContestModel.query.filter_by(
            url=url
        ).first()
        if not contest:
            return response_with(responses.SERVER_ERROR_404, value={
                "error_message": "Resource does not exists"
            })
        contest_schema = ContestSchema()
        contest = contest_schema.dump(contest)
        return response_with(responses.SUCCESS_200, value={
            "contest": contest
        })

    @jwt_required
    def put(self, url):
        admin_id = get_jwt_identity()
        contest = ContestModel.query.filter_by(
            url=url, admin=admin_id
        ).first()
        if not contest:
            return response_with(responses.SERVER_ERROR_404, value={
                "error_message": "Resource does not exists"
            })
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

    @jwt_required
    def delete(self, url):
        admin_id = get_jwt_identity()
        contest = ContestModel.query.filter_by(
            url=url, admin=admin_id
        ).first()
        if not contest:
            return response_with(responses.SERVER_ERROR_404, value={
                "error_message": "Resource does not exists"
            })
        db.session.delete(contest)
        db.session.commit()
        return response_with(responses.SUCCESS_204)















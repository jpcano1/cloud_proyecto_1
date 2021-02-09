from flask_restful import Resource
from flask import request
from ..utils import db, responses, response_with
from sqlalchemy.exc import IntegrityError
from ..utils import responses, db, response_with
from ..models import Contest
from ..models import ContestSchema


class Contest(Resource):
    def get(self):
        contests = Contest.query.all()
        contes_schema = ContestSchema(many = True)
        contests = contes_schema.dump(contests)
        return response_with(responses.SUCCESS_200, value={
            "contests": contests
        })

    def post(self):
        data = request.get_json()
        if (not data.get("name") or not data.get("url")
            or not data.get("begin_date") or not data.get("end_date") or not data.get("prize")
            or not data.get("script")):
            return response_with(responses.MISSING_PARAMETERS_422)
        contest_schema = ContestSchema()
        contest = contest_schema.load( data, session = db.session)

        try:
            contest.create()
        except IntegrityError:
            return response_with(responses.INVALID_FIELD_NAME_SENT_422, value={
                "error_message": "Url already exists"
            })
        except Exception as e:
            return response_with(responses.INVALID_INPUT_422, value={
                "error_message": str(e)
            })
        return response_with(responses.SUCCESS_200, value={
            "message": "Contest created"
        })







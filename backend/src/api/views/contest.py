from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError
from ..utils import responses, db, response_with
from ..models import Contest as ContestModel
from ..models import ContestSchema


class Contest(Resource):
    def get(self):
        contests = ContestModel.query.all()
        contes_schema = ContestSchema(many = True)
        contests = contes_schema.dump(contests)
        return response_with(responses.SUCCESS_200, value={
            "contests": contests
        })

    def post(self):
        data = request.get_json()
        data["admin"] = ""
        if (not data.get("name") or not data.get("url")
            or not data.get("begin_date") or not data.get("end_date") or not data.get("prize")
            or not data.get("script")):
            return response_with(responses.MISSING_PARAMETERS_422)
        contest_schema = ContestSchema()
        contest = contest_schema.load(data, session=db.session)

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

class ContestDetail(Resource):
    def get(self, url):
        contest = ContestModel.query.filter_by(url=url).first()
        if not contest:
            return response_with(responses.SERVER_ERROR_404, value={
                "error_message": "Resource does not exists"
            })
        contest_schema = ContestSchema()
        contest = contest_schema.dump(contest)
        return response_with(responses.SUCCESS_200, value={
            "contest": contest
        })






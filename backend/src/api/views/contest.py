from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError
from ..utils import responses, db, response_with
from ..models import Contest as ContestModel
from ..models import ContestSchema
from datetime import datetime as dt


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
        if (not data.get("name") or not data.get("url")
            or not data.get("begin_date") or not data.get("end_date") or not data.get("prize")
            or not data.get("script")):
            return response_with(responses.MISSING_PARAMETERS_422)
        data["admin"] = 1
        contest_schema = ContestSchema()
        contest = contest_schema.load(data, session=db.session)

        try:
            db.session.add(contest)
            db.session.commit()
            contest = contest_schema.dump(contest)
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
            "contest": contest
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
    def put(self, url):
        contest = ContestModel.query.filter_by(url=url).first()
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
    def delete(self,url):
        contest = ContestModel.query.filter_by(url=url).first()
        if not contest:
            return response_with(responses.SERVER_ERROR_404, value={
                "error_message": "Resource does not exists"
            })
        db.session.delete(contest)
        db.session.commit()
        return response_with(responses.SUCCESS_204)















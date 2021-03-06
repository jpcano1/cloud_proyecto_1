import json
from ..utils.test_base import BaseTestCase
from ..models import Admin, Contest
import unittest2 as unittest
from .test_admins import create_admins
from datetime import datetime

def create_contests():
    begin_date = datetime.strptime("1/1/2021", "%d/%m/%Y")
    end_date = datetime.strptime("2/1/2021", "%d/%m/%Y")
    Contest(
        name="Contest", url="url", begin_date=begin_date,
        end_date=end_date, prize=2000, script="script",
        recommendations="recommendations", admin=1
    ).create()

    Contest(
        name="Contest", url="url1", begin_date=begin_date,
        end_date=end_date, prize=2000, script="script",
        recommendations="recommendations", admin=2
    ).create()

class TestContests(BaseTestCase):
    def login(self):
        admin = {
            "email": "name_1@email.com",
            "password": "name_last_name_1"
        }

        response = self.app.post(
            "/api/login",
            data=json.dumps(admin),
            content_type="application/json",
        )

        return json.loads(response.data)

    def setUp(self):
        super(TestContests, self).setUp()
        create_admins()
        create_contests()
        self.access_token = self.login()["access_token"]

    def test_create_contest(self):
        contest = {
            "name": "Contest",
            "url": "url2",
            "begin_date": "1/1/2021",
            "end_date": "2/1/2021",
            "prize": 2000,
            "script": "script",
            "recommendations": "recommendations"
        }

        response = self.app.post(
            "/api/contest",
            data=json.dumps(contest),
            content_type="application/json",
        )

        self.assertEqual(401, response.status_code)

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        response = self.app.post(
            "/api/contest",
            data=json.dumps(contest),
            content_type="application/json",
            headers=headers
        )

        self.assertEqual(200, response.status_code)

    def test_create_existing_contest(self):
        contest = {
            "name": "Contest",
            "url": "url",
            "begin_date": "1/1/2021",
            "end_date": "2/1/2021",
            "prize": 2000,
            "script": "script",
            "recommendations": "recommendations"
        }

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        response = self.app.post(
            "/api/contest",
            data=json.dumps(contest),
            content_type="application/json",
            headers=headers
        )

        self.assertEqual(422, response.status_code)

    def test_create_contest_invalid_fields(self):
        contest = {
            "name": "Contest",
            "url": "url2",
            "begin_date": "1/1/2021",
            "end_date": "2/1/2020",
            "prize": 2000,
            "recommendations": "recommendations"
        }

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        response = self.app.post(
            "/api/contest",
            data=json.dumps(contest),
            content_type="application/json",
            headers=headers
        )

        self.assertEqual(422, response.status_code)

    def test_get_contest(self):
        response = self.app.get(
            "/api/contest",
        )

        data = json.loads(response.data)
        self.assertEqual(2, len(data["contests"]))
        self.assertEqual(200, response.status_code)

if __name__ == "__main__":
    unittest.main()
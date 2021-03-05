import json
from ..utils.test_base import BaseTestCase
from ..models import Admin
import unittest2 as unittest

def create_admins():
    Admin(
        name="Name 1", last_name="Last Name 1",
        email="name_1@email.com",
        password=Admin.generate_hash("name_last_name_1")
    ).create()
    Admin(
        name="Name 2", last_name="Last Name 2",
        email="name_2@email.com",
        password=Admin.generate_hash("name_last_name_2")
    ).create()

class TestAdmins(BaseTestCase):
    def setUp(self):
        super(TestAdmins, self).setUp()
        create_admins()

    def test_login_admin(self):
        admin = {
            "email": "name_1@email.com",
            "password": "name_last_name_1"
        }
        response = self.app.post(
            "/api/login",
            data=json.dumps(admin),
            content_type="application/json"
        )
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("access_token" in data)

    def test_login_wrong_credentials(self):
        admin = {
            "email": "name_1@email.com",
            "password": "pass"
        }

        response = self.app.post(
            "/api/login",
            data=json.dumps(admin),
            content_type="application/json"
        )
        self.assertEqual(422, response.status_code)

    def test_create_user(self):
        admin = {
            "email": "test@email.com",
            "password": "hola",
            "name": "Name",
            "last_name": "Last Name"
        }

        response = self.app.post(
            "/api/signup",
            data=json.dumps(admin),
            content_type="application/json"
        )
        data = json.loads(response.data)

        self.assertEqual(201, response.status_code)
        self.assertTrue("success" in data["code"])

    def test_create_existing_user(self):
        admin = {
            "email": "name_1@email.com",
            "name": "Name 1",
            "last_name": "Last Name 1",
            "password": "name_last_name_1"
        }

        response = self.app.post(
            "/api/signup",
            data=json.dumps(admin),
            content_type="application/json"
        )

        data = json.loads(response.data)
        self.assertEqual(422, response.status_code)
        self.assertTrue("Email already exists" in data["errors"])

    def test_create_admin_without_fields(self):
        admin = {
            "password": "hola",
            "name": "Name",
            "last_name": "Last Name"
        }

        response = self.app.post(
            "/api/signup",
            data=json.dumps(admin),
            content_type="application/json"
        )

        data = json.loads(response.data)
        self.assertEqual(422, response.status_code)
        self.assertTrue("email" in data["errors"])

        admin = {
            "email": "test@email.com",
            "name": "Name",
            "last_name": "Last Name"
        }

        response = self.app.post(
            "/api/signup",
            data=json.dumps(admin),
            content_type="application/json"
        )

        data = json.loads(response.data)
        self.assertEqual(422, response.status_code)
        self.assertTrue("password" in data["errors"])

    def test_get_admin(self):
        response = self.app.get(
            "/api/admin"
        )

        data = json.loads(response.data)
        self.assertEqual(2, len(data["admins"]))
        self.assertEqual(200, response.status_code)

    def tearDown(self):
        super(TestAdmins, self).tearDown()

if __name__ == "__main__":
    unittest.main()
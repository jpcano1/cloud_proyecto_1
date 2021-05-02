from ..models import AdminModel
from datetime import timedelta
from flask_jwt_extended import create_access_token



class AdminController:
    def __init__(self):
        self.admin_model = AdminModel()

    def signup(self, data: dict):
        fetched_admin = self.admin_model.find_by_email(data["email"])

        if fetched_admin:
            raise ValueError("User already exists")
        data["password"] = self.admin_model.generate_hash(data["password"])
        admin = self.admin_model.create(data)
        return admin

    def login(self, data):
        fetched_admin = self.admin_model.find_by_email(data["email"])

        if not fetched_admin:
            raise ValueError("Wrong email or password")
        verification = self.admin_model.verify_hash(
            fetched_admin["password"],
            data["password"]
        )
        if not verification:
            raise ValueError("Wrong email or password")

        expires = timedelta(hours=4)
        access_token = create_access_token(
            identity=str(fetched_admin["email"]),
            expires_delta=expires
        )
        return {
            "admin_id": str(fetched_admin["email"]),
            "access_token": access_token
        }
    def get(self, email):
        fetched_admin = self.admin_model.find_one(email)
        if not fetched_admin:
            raise ValueError("User not found")
        return self.admin_model.to_dict(fetched_admin)

    def list(self):
        result = self.admin_model.find()
        return [self.admin_model.to_dict(x) for x in result]

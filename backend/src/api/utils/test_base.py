import unittest2 as unittest
from ..config import TestingConfig
from . import db, create_app
import tempfile
import os

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app(TestingConfig)
        self.test_db_file = tempfile.mkstemp()[1]
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.abspath(self.test_db_file)

        db.init_app(app)
        with app.app_context():
            db.create_all()

        app.app_context().push()
        self.app = app.test_client()

    def tearDown(self):
        db.session.close_all()
        db.drop_all()
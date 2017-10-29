# Filename: __init__.py

# Standard libraries
import os

# Flask Testing
from flask_testing import TestCase

# Globe Indexer
from globe_indexer import app
from globe_indexer import db
from globe_indexer.api import database


class BaseTest(TestCase):
    def create_app(self):
        app.config.from_object('config.TestConfig')
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()
        input_fpath = os.path.join(os.path.dirname(__file__), 'data',
                                   'geoname_example.txt')
        database.initialize_db(db, input_fpath)
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

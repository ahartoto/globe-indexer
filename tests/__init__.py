# Filename: __init__.py

# Standard libraries
import os

# Flask
import flask

# Flask Testing
from flask_testing import TestCase

# Globe Indexer
from globe_indexer.api import database
from globe_indexer.api.controllers import api as api_blueprint
from globe_indexer.api.models import db


class BaseTest(TestCase):
    def create_app(self):
        app = flask.Flask(__name__)
        app.config.from_object('config.TestConfig')
        app.register_blueprint(api_blueprint)
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()
        input_fpath = os.path.join(os.path.dirname(__file__), 'data',
                                   'geoname_example.txt')
        database.initialize_db(db, input_fpath)
        self.app = flask.current_app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

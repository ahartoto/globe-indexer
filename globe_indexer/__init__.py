"""
Globe Indexer Application
"""

# Standard libraries
import os

# Flask
import flask

# SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Version
__version__ = "0.0.1"

# Application
app = flask.Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
app.config.from_envvar('GLOBE_INDEXER_CONFIG_FILE', silent=True)

# Database
db = SQLAlchemy(app)

# pylint: disable=wrong-import-position
from .api.controllers import api as api_blueprint
from .api.database import initialize_db
# pylint: enable=wrong-import-position

# Register Blueprint
app.register_blueprint(api_blueprint)

# Initialize database
db.create_all()
initialize_db(db, os.path.join(os.path.dirname(__file__), 'input',
                               'cities1000.txt'))

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
app.config.from_object('config.BaseConfig')
if os.path.exists(os.path.join(app.instance_path, 'config.py')):
    app.config.from_pyfile('config.py')
app.config.from_envvar('GLOBE_INDEXER_CONFIG_FILE', silent=True)


# pylint: disable=unused-argument
@app.errorhandler(404)
def page_not_found(error):
    """
    Default handler of non-existing page/path.

    :param error: value to be passed to decorator
    :returns: Flask response
    """
    payload = {
        'error': 'cannot find the resource',
        'type': 'INVALID_PATH',
    }
    return flask.jsonify(payload), 404
# pylint: enable=unused-argument


# Database
db = SQLAlchemy()

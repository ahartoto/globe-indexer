# Filename: run.py

# Standard libraries
import os

# Flask
import flask

# Globe Indexer
from globe_indexer.api.controllers import api as api_blueprint
from globe_indexer.api.database import initialize_db


# Interface functions
def create_app():
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.BaseConfig')
    if os.path.exists(os.path.join(app.instance_path, 'config.py')):
        app.config.from_pyfile('config.py')
    app.config.from_envvar('GLOBE_INDEXER_CONFIG_FILE', silent=True)

    from globe_indexer.api.models import db
    db.init_app(app)

    # Initialize database
    with app.app_context():
        db.create_all()
        initialize_db(db, os.path.join(os.path.dirname(__file__), 'input',
                                       'cities1000.txt'))

    app.register_blueprint(api_blueprint)
    return app


# Create application
application = create_app()


@application.errorhandler(404)
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


def main():
    """
    Main function for the application
    """
    # Run the application
    application.run()


# Entry point
if __name__ == '__main__':
    main()

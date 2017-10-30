# Filename: run.py

# Standard libraries
import os

# Globe Indexer
from globe_indexer import app as application
from globe_indexer import db
from globe_indexer.api.controllers import api as api_blueprint
from globe_indexer.api.database import initialize_db


# Interface functions
def main():
    """
    Main function for the application
    """
    # Add application to context for database
    application.app_context().push()

    # Register Blueprint
    application.register_blueprint(api_blueprint)

    # Initialize database
    db.init_app(application)
    db.create_all()
    initialize_db(db, os.path.join(os.path.dirname(__file__), 'input',
                                   'cities1000.txt'))

    # Run the application
    application.run()


# Entry point
if __name__ == '__main__':
    main()

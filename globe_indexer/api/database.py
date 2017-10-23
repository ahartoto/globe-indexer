# Filename: database.py

"""
Globe Indexer API Database Module

Interface functions:
    initialize_db
"""

# Standard libraries
import os

# Globe Indexer
from globe_indexer.api.models import GeoName
from globe_indexer.error import GlobeIndexerError
from globe_indexer.utils import parse_geoname_table_file


# Interface functions
def initialize_db(db, fpath, **kwargs):
    """
    Initialize the content of the database if none exists.

    :param db: instance of :class:`flask_alchemy.SQLAlchemy`
    :param fpath: string - Path to the input csv/text file
    :param kwargs: dict - extra arguments to be passed to
                   :function:`utils.parse_geoname_table_file`
    """
    if not os.path.isfile(fpath):
        fstr = "path is not a file: {}".format(fpath)
        raise GlobeIndexerError(fstr)

    # Load the data if none is present
    if db.session.query(GeoName).count() == 0:
        for row in parse_geoname_table_file(fpath, **kwargs):
            point = GeoName(row)
            db.session.add(point)
        db.session.commit()

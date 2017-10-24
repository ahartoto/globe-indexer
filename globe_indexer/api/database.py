# Filename: database.py

"""
Globe Indexer API Database Module

Interface functions:
    initialize_db
"""

# Standard libraries
import os

# Globe Indexer
from globe_indexer.config import DATA_SET_URL
from globe_indexer.api.models import GeoName
from globe_indexer.error import GlobeIndexerError
from globe_indexer.utils import download_file, parse_geoname_table_file, unzip


# Interface functions
def initialize_db(db, fpath, **kwargs):
    """
    Initialize the content of the database if none exists.

    :param db: instance of :class:`flask_alchemy.SQLAlchemy`
    :param fpath: string - Path to the input csv/text file
    :param kwargs: dict - extra arguments to be passed to
                   :function:`utils.parse_geoname_table_file`
    """
    # Load the data if none is present
    if db.session.query(GeoName).count() == 0:
        if not os.path.isfile(fpath):
            # download from the source and place it in the fpath
            zip_fpath = os.path.join(os.path.dirname(fpath), 'cities.zip')
            download_file(DATA_SET_URL, zip_fpath)
            unzip(zip_fpath, os.path.dirname(fpath))

            if not os.path.isfile(fpath):
                fstr = "cannot retrieve the file: {}".format(fpath)
                raise GlobeIndexerError(fstr)

        for row in parse_geoname_table_file(fpath, **kwargs):
            point = GeoName(row)
            db.session.add(point)
        db.session.commit()

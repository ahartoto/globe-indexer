# Filename: utils.py

"""
Globe Indexer Utility Module

Interface functions:
    haversine
    parse_geoname_table_file
"""

# Standard libraries
import csv
import math
import os

# Globe Indexer
from globe_indexer import config
from globe_indexer.error import GlobeIndexerError


GEONAME_TABLE_HEADERS = (
    'geonameid',
    'name',
    'asciiname',
    'alternatenames',
    'latitude',
    'longitude',
    'feature_class',
    'feature_code',
    'country_code',
    'cc2',
    'admin1_code',
    'admin2_code',
    'admin3_code',
    'admin4_code',
    'population',
    'elevation',
    'dem',
    'timezone',
    'modification_date',
)


def get_distance(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points on the earth
    (specified in decimal degrees)

    :param lon1: longitude of first point
    :param lat1: latitude of first point
    :param lon2: longitude of second point
    :param lat2: latitude of second point
    :returns: float
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # Use Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + \
        math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return c * config.EARTH_RADIUS


def parse_geoname_table_file(fpath, delimiter='\t'):
    """
    Parse the table given in a file

    :param fpath: string - path to the file
    :param delimiter: string - delimiter between columns in the file
    :returns: list of dict
    """
    if not os.path.isfile(fpath):
        fstr = "path is not a file: {}".format(fpath)
        raise GlobeIndexerError(fstr)

    full_fpath = os.path.realpath(fpath)
    rows = list()
    with open(full_fpath) as fin:
        reader = csv.DictReader(fin, fieldnames=GEONAME_TABLE_HEADERS,
                                delimiter=delimiter, quoting=csv.QUOTE_NONE)
        for line in reader:
            rows.append(line)

    return rows

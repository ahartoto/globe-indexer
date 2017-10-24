# Filename: utils.py

"""
Globe Indexer Utility Module

Interface functions:
    download_file
    get_distance
    mkdirs
    parse_geoname_table_file
    unzip
"""

# Standard libraries
import csv
import math
import os
import zipfile

# Requests
import requests

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


def download_file(url, fpath):
    """
    Download file from the specified URL (assuming that there is no
    authorization required)

    :param url: string - URL of the resource
    :param fpath: string - path to where to place the file
    """
    mkdirs(os.path.dirname(fpath))

    response = requests.get(url, stream=True)
    with open(fpath, mode='wb') as fout:
        for chunk in response.iter_content(chunk_size=config.DATA_CHUNK_SIZE):
            if chunk:
                fout.write(chunk)


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
    value = math.sin(dlat / 2) ** 2 + \
        math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    value = 2 * math.asin(math.sqrt(value))
    return value * config.EARTH_RADIUS


def mkdirs(dpath):
    """
    Create directory path (including the path of the parent directory if it
    doesn't already exist)

    :param dpath: string - path to directory to be created
    """
    if os.path.isdir(dpath):
        return

    try:
        os.makedirs(dpath)
    except OSError as exc:
        fstr = "cannot create directory: {}".format(dpath)
        raise GlobeIndexerError(fstr, details=str(exc))


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


def unzip(fpath, dpath):
    """
    Unzip all files in the zip file at the specified directory

    :param fpath: string - path to zip file
    :param dpath: string - output path
    """
    mkdirs(dpath)
    with zipfile.ZipFile(fpath) as zip_fin:
        zip_fin.extractall(path=dpath)

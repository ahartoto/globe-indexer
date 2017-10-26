# Filename: query.py

"""
Globe Indexer API Query Module
"""

# PyCountry
import pycountry

# SQLAlchemy
from sqlalchemy import distinct

# Globe indexer
from globe_indexer import db
from globe_indexer import utils
from globe_indexer.api.models import GeoName
from globe_indexer.error import GlobeIndexerError


# Interface functions
def country_code_query():
    """
    Get all country codes

    :returns: list of string
    """
    # pylint: disable=no-member
    query = db.session.query(distinct(GeoName.country_code))
    # pylint: enable=no-member

    codes = [('', '')]
    for code in query.order_by(GeoName.country_code):
        try:
            country_name = pycountry.countries.get(alpha_2=code[0]).name
        except KeyError:
            country_name = code[0]
        choice = '{} - {}'.format(code[0], country_name)
        codes.append((code[0], choice))
    return codes


def lexical_query(names):
    """
    Perform lexical search based on the name provided by the user.

    :param names: list of string
    :returns: iterable of query
    """
    if len(names) == 1:
        value = names[0]
    else:
        value = '%'.join(names)

    query = GeoName.query.filter(GeoName.name.ilike(value))
    results = query.order_by(GeoName.id).all()
    return results


def proximity_query(geoname_id, country_code=None):
    """
    Get all cities sorted by their distances from the city whose ID is given.

    :param geoname_id: int
    :param country_code: string
    :returns: a sorted tuple where each element is a tuple of float and int.
              The float value signifies the distance between the city with the
              specified ID. The integer value is the ID of the city.
    """
    result = GeoName.query.filter_by(id=geoname_id).first()
    if not result:
        fstr = "cannot find city with ID: {}".format(geoname_id)
        raise GlobeIndexerError(fstr)

    # Get all points in the table
    # pylint: disable=no-member
    query = db.session.query(GeoName.id, GeoName.latitude,
                             GeoName.longitude)
    # pylint: enable=no-member
    if country_code is None:
        results = query.all()
    else:
        results = query.filter_by(country_code=country_code).all()

    distances = list()
    for other_id, other_lat, other_long in results:
        if other_id == geoname_id:
            continue
        distances.append((utils.get_distance(result.longitude, result.latitude,
                                             other_long, other_lat),
                          other_id))

    return sorted(distances)

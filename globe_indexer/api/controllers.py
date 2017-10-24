# Filename: controllers.py

"""
Globe Indexer API Controller Module
"""

# Standard libraries
import http
import os

# Flask
import flask

# SQLAlchemy
from sqlalchemy import and_, or_

# Globe Indexer
from globe_indexer import config
from globe_indexer import db
from globe_indexer import utils
from globe_indexer.api.models import GeoName


# Constants
api = flask.Blueprint('api', __name__)


# Icon for the website
# taken from http://findicons.com/files/icons/98/nx11/256/internet_real.png
@api.route('/favicon.ico')
def favicon():
    """
    Return the icon used to distinguish this application
    :returns: Flask response
    """
    return flask.send_from_directory(os.path.join(api.root_path, 'static'),
                                     'favicon.ico',
                                     mimetype='image/vnd.microsoft.icon')


@api.route('/<int:geoname_id>')
def geoname(geoname_id):
    """
    Get the resource information of a city given an ID

    :param geoname_id: int - ID associated with a city
    :returns: Flask response
    """
    result = GeoName.query.filter_by(id=geoname_id).first()
    if not result:
        payload = {
            'error': {
                'message': "no city is found with ID: {}".format(geoname_id),
                'type': 'INVALID_PATH',
            }
        }
        return flask.jsonify(payload), http.HTTPStatus.NOT_FOUND

    return result.json()


@api.route('/health')
def health():
    """
    Endpoint to help checking the health of our app when it's deployed

    :returns: Flask response
    """
    return flask.jsonify({'message': 'API is available'})


@api.route('/lexical')
def lexical():
    """
    Get the information of cities that are matching the specified keywords.

    :returns: Flask response
    """
    if not flask.request.query_string:
        payload = {
            'error': {
                'message': 'no cityName query string was provided',
                'type': 'MISSING_QUERY_PARAMETER',
            }
        }
        return flask.jsonify(payload), http.HTTPStatus.BAD_REQUEST

    extra_query_params = [key for key in flask.request.args
                          if key not in {'cityName'}]
    if extra_query_params:
        payload = {
            'error': {
                'message': 'invalid query parameters: {}'.format(
                    ','.join(extra_query_params)),
                'type': 'UNSUPPORTED_QUERY_PARAMETER',
            }
        }
        return flask.jsonify(payload), http.HTTPStatus.BAD_REQUEST

    names = [name.lower() for name in flask.request.args['cityName'].split()]
    if len(names) < 1:
        payload = {
            'error': {
                'message': 'no value was provided to cityName query parameter',
                'type': 'VALIDATION_ERROR',
            }
        }
        return flask.jsonify(payload), http.HTTPStatus.BAD_REQUEST
    elif len(names) == 1:
        name = '%{}%'.format(names[0])
        all_criteria = or_(GeoName.name.ilike(name),
                           GeoName.ascii_name.ilike(name),
                           GeoName.alternate_names.ilike(name))
        result = GeoName.query.filter(all_criteria).order_by(GeoName.id)
    else:
        search_criteria = [GeoName.name.ilike('%{}%'.format(name))
                           for name in names]
        all_criteria = and_(*search_criteria)
        search_criteria = [GeoName.ascii_name.ilike('%{}%'.format(name))
                           for name in names]
        all_criteria = or_(all_criteria, and_(*search_criteria))
        search_criteria += [GeoName.alternate_names.ilike('%{}%'.format(name))
                            for name in names]
        all_criteria = or_(all_criteria, and_(*search_criteria))
        result = GeoName.query.filter(all_criteria).order_by(GeoName.id)

    points = [point.json() for point in result]
    return flask.jsonify({'cities': points, 'total': len(points)})


@api.route('/proximity/<int:geoname_id>')
def proximity(geoname_id):
    """
    Get cities closest to the specified one.

    :param geoname_id: int - ID associated with a city
    :returns: Flask response
    """
    extra_query_params = [key for key in flask.request.args
                          if key not in {'k', 'countryCode'}]
    if extra_query_params:
        payload = {
            'error': {
                'message': 'invalid query parameters: {}'.format(
                    ','.join(extra_query_params)),
                'type': 'UNSUPPORTED_QUERY_PARAMETER',
            }
        }
        return flask.jsonify(payload), http.HTTPStatus.BAD_REQUEST

    try:
        k = int(flask.request.args['k'])
        if k < 1:
            raise ValueError("invalid value for parameter k")
    except KeyError:
        # Choose default
        k = config.DEFAULT_PROXIMITY_LIMIT
    except ValueError:
        payload = {
            'error': {
                'message': "query parameter 'k' needs to be a positive "
                           "integer: {}".format(flask.request.args['k']),
                'type': 'VALIDATION_ERROR',
            }
        }
        return flask.jsonify(payload), http.HTTPStatus.BAD_REQUEST

    try:
        country_code = str(flask.request.args['countryCode']).upper()
    except KeyError:
        country_code = None

    result = GeoName.query.filter_by(id=geoname_id).first()
    if not result:
        payload = {
            'error': {
                'message': "no city is found with ID: {}".format(geoname_id),
                'type': 'INVALID_PATH',
            }
        }
        return flask.jsonify(payload), http.HTTPStatus.NOT_FOUND

    # Get all points in the table
    # pylint: disable=no-member
    query = db.session.query(GeoName.id, GeoName.latitude,
                             GeoName.longitude)
    # pylint: enable=no-member
    if country_code is None:
        points = query.all()
    else:
        points = query.filter_by(country_code=country_code).all()

    distances = list()
    for other_id, other_lat, other_long in points:
        if other_id == geoname_id:
            continue
        distances.append((utils.get_distance(result.longitude, result.latitude,
                                             other_long, other_lat),
                          other_id))

    cities = [{'city': GeoName.query.filter_by(id=distance[1]).first().json(),
               'distance': distance[0]}
              for distance in sorted(distances)[:k]]
    return flask.jsonify({'cities': cities,
                          'limit': k,
                          'total_available': len(distances)})
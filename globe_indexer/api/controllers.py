# Filename: controllers.py

"""
Globe Indexer API Controller Module
"""

# Standard libraries
import json
import os

# Python 3.5+
try:
    from http import HTTPStatus as StatusCodes
except ImportError:
    # Python 3
    from http import client as StatusCodes

# Flask
import flask

# Globe Indexer
from globe_indexer import config
from globe_indexer import utils
from globe_indexer.api.forms import LexicalForm, ProximityForm
from globe_indexer.api.models import GeoName
from globe_indexer.api.query import (
    country_code_query,
    lexical_query,
    proximity_query,
)
from globe_indexer.error import GlobeIndexerError

# Constants
api = flask.Blueprint('api', __name__,
                      static_folder='static', template_folder='templates')


@api.route('/form/proximity', methods=['GET', 'POST'])
def proximity_form():
    """
    Serve the page to the user to provide entry point for querying information

    :returns: rendering of the page
    """
    center = None
    cities = list()

    form = ProximityForm()
    form.country_code.choices = country_code_query()

    kwargs = {
        'center': center,
        'cities': cities,
        'enumerate': enumerate,
        'proximity_form': form,
    }

    template_fname = 'proximity.html'

    if form.validate_on_submit():
        try:
            geoname_id = int(form.geoname_id.data)
        except ValueError:
            flask.flash("city ID should be an integer", "error")
            return flask.render_template(template_fname, **kwargs)

        try:
            k = int(form.query_limit.data)
            if k < 1:
                raise ValueError("value of search limit should be a positive "
                                 "integer")
        except ValueError as exc:
            flask.flash(str(exc), "error")
            return flask.render_template(template_fname, **kwargs)

        country_code = None
        if form.country_code.data:
            country_code = form.country_code.data.upper()
            if len(country_code) != 2:
                flask.flash("invalid country code format provided", "error")
                return flask.render_template(template_fname, **kwargs)

        center = GeoName.query.filter_by(id=geoname_id).first()
        if center:
            results = proximity_query(geoname_id, country_code=country_code)
            cities = [GeoName.query.filter_by(id=elem[1]).first()
                      for elem in results[:k]]
            kwargs['center'] = center
            kwargs['cities'] = cities
        else:
            flask.flash("Cannot find city with the given ID. Try again",
                        "error")
    return flask.render_template(template_fname, **kwargs)


@api.route('/', methods=['GET', 'POST'])
@api.route('/form/lexical', methods=['GET', 'POST'])
def lexical_form():
    """
    Serve the page to the user to provide entry point for querying information

    :returns: rendering of the page
    """
    form = LexicalForm()
    cities = list()
    response = None
    if form.validate_on_submit():
        value = form.name.data
        if utils.has_invalid_chars(value):
            flask.flash("city name can only be alphanumeric or * character",
                        "error")
        else:
            names = [name.lower() for name in value.split()]
            cities = lexical_query(names)
            if cities:
                payload = {
                    'cities': [city.json() for city in cities],
                    'total': len(cities),
                }
                response = json.dumps(payload, ensure_ascii=False, indent=2)
            else:
                flask.flash("Found no city with the specified name. Try a "
                            "different one or use the * wildcard.",
                            "message")
    return flask.render_template('lexical.html', cities=cities,
                                 response=response, lexical_form=form)


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
        message = "no city is found with ID: {}".format(geoname_id)
        error_type = 'INVALID_PATH'
        return utils.formulate_json_error(message, error_type,
                                          StatusCodes.NOT_FOUND)

    return flask.jsonify(result.json(compact=False))


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
        message = 'no cityName query string was provided'
        error_type = 'MISSING_QUERY_PARAMETER'
        return utils.formulate_json_error(message, error_type,
                                          StatusCodes.BAD_REQUEST)

    extra_query_params = [key for key in flask.request.args
                          if key not in {'cityName'}]
    if extra_query_params:
        message = 'invalid query parameters: {}'.format(
            ','.join(extra_query_params))
        error_type = 'UNSUPPORTED_QUERY_PARAMETER'
        return utils.formulate_json_error(message, error_type,
                                          StatusCodes.BAD_REQUEST)

    city_name = flask.request.args['cityName']
    if utils.has_invalid_chars(city_name):
        message = 'found invalid chars in parameter: {}'.format(city_name)
        message += '. Valid chars: A-Za-z0-9*'
        error_type = 'VALIDATION_ERROR'
        return utils.formulate_json_error(message, error_type,
                                          StatusCodes.BAD_REQUEST)

    words = [word.lower() for word in city_name.split()]
    if not words:
        message = 'no value was provided to cityName query parameter'
        error_type = 'VALIDATION_ERROR'
        return utils.formulate_json_error(message, error_type,
                                          StatusCodes.BAD_REQUEST)

    results = lexical_query(words)
    if not results:
        message = 'found no city with the provided name: {}'.format(city_name)
        error_type = 'INVALID_PARAMETER_VALUE'
        return utils.formulate_json_error(message, error_type,
                                          StatusCodes.NOT_FOUND)

    cities = [city.json() for city in results]
    return flask.jsonify({'cities': cities, 'total': len(cities)})


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
        message = 'invalid query parameters: {}'.format(
            ','.join(extra_query_params))
        error_type = 'UNSUPPORTED_QUERY_PARAMETER'
        return utils.formulate_json_error(message, error_type,
                                          StatusCodes.BAD_REQUEST)

    try:
        k = int(flask.request.args['k'])
        if k < 1:
            raise ValueError("invalid value for parameter k")
    except KeyError:
        # Choose default
        k = config.DEFAULT_PROXIMITY_LIMIT
    except ValueError:
        message = "query parameter 'k' needs to be a positive " \
                  "integer: {}".format(flask.request.args['k'])
        error_type = 'VALIDATION_ERROR'
        return utils.formulate_json_error(message, error_type,
                                          StatusCodes.BAD_REQUEST)

    try:
        country_code = str(flask.request.args['countryCode']).upper()
    except KeyError:
        country_code = None

    try:
        values = proximity_query(geoname_id, country_code=country_code)
    except GlobeIndexerError as exc:
        error_type = 'INVALID_PARAMETER_VALUE'
        return utils.formulate_json_error(exc.message, error_type,
                                          StatusCodes.BAD_REQUEST)

    cities = [{'city': GeoName.query.filter_by(id=value[1]).first().json(),
               'distance': value[0]}
              for value in values[:k]]

    return flask.jsonify({'cities': cities, 'limit': k,
                          'total_available': len(values)})


@api.route('/static/style.css')
def style_css():
    """
    Return the style.css
    :returns: Flask response
    """
    return flask.send_from_directory(os.path.join(api.root_path, 'static'),
                                     'style.css')

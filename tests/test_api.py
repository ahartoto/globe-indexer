# Filename: test_api.py

"""
Test content of the api/controllers.py for REST APIs
"""

# Standard libraries
import json

# Globe Indexer
from globe_indexer import config
from globe_indexer.api.models import GeoName

# Test
from . import BaseTest


class TestAPI(BaseTest):
    def test_health(self):
        response = self.app.get('/health')
        self.assert200(response, "Service is supposed to be running")

        payload = {'message': 'API is available'}
        self.assertEqual(json.loads(response.data.decode()),
                         json.loads(json.dumps(payload)),
                         "Health returns unexpected message")

    def test_id(self):
        city_id = 3040132
        city = GeoName.query.filter_by(id=city_id).first()

        response = self.app.get('/{}'.format(city_id))
        self.assert200(response, "Valid city ID should return 200")
        assert json.loads(response.data.decode()) == city.json(compact=False)

        city_id = 0
        response = self.app.get('/{}'.format(city_id))
        self.assert404(response, "Invalid ID should return 404")
        payload = {
            'error': {
                'message': 'no city is found with ID: {}'.format(city_id),
                'type': 'INVALID_PATH'
            }
        }
        self.assertEqual(json.loads(response.data.decode()),
                         json.loads(json.dumps(payload)),
                         "Invalid ID returns unexpected message")

    def test_lexical(self):
        response = self.app.get('/lexical')
        self.assert400(response, "No query parameter should return 400")

        response = self.app.get('/lexical?cityName')
        self.assert400(response, "cityName parameter with no value should "
                                 "return 400")

        response = self.app.get('/lexical?cityName=')
        self.assert400(response, "cityName parameter with no value should "
                                 "return 400")

        response = self.app.get('/lexical?foo=bar')
        self.assert400(response, "unsupported parameter should return 400")

        response = self.app.get('/lexical?cityName=El Tarter&blah=0')
        self.assert400(response, "extra parameter should return 400")

        response = self.app.get('/lexical?blah=0&cityName=El Tarter')
        self.assert400(response, "extra parameter version 2 should return 400")

        response = self.app.get('/lexical?cityName=Nowhere')
        self.assert404(response, "city not in db should return 404")

        city_name = 'Encamp'
        response = self.app.get('/lexical?cityName={}'.format(city_name))
        self.assert200(response, "valid city name should return 200")

        payload = {
            'cities': [
                GeoName.query.filter_by(name=city_name).first().json()
            ],
            'total': 1,
        }
        self.assertEqual(json.loads(response.data.decode()),
                         json.loads(json.dumps(payload)),
                         "valid city response has unexpected JSON content")

        city_name = 'Sant Julià de Lòria'
        response = self.app.get('/lexical?cityName={}'.format(city_name))
        self.assert200(response, "city with non ASCII character is supported")

    def test_proximity(self):
        response = self.app.get('/proximity')
        self.assert404(response, "No city ID for proximity should return 400")

        city_id = 0
        response = self.app.get('/proximity/{}'.format(city_id))
        self.assert400(response, "invalid city ID should return 400")

        response = self.app.get('/proximity/124foo')
        self.assert404(response, "non-number city ID should return 404")

        city_id = 3039163
        response = self.app.get('/proximity/{}'.format(city_id))
        self.assert200(response, "valid city ID returns 200")
        payload = json.loads(response.data.decode())
        assert payload['limit'] == config.DEFAULT_PROXIMITY_LIMIT
        assert payload['total_available'] == 8
        assert len(payload['cities']) == payload['limit']

        last_distance = payload['cities'][0]['distance']
        for city in payload['cities'][1:]:
            assert last_distance <= city['distance']
            last_distance = city['distance']

        k = 0
        response = self.app.get('/proximity/{}?k={}'.format(city_id, k))
        self.assert400(response, "invalid k value should return 400")

        k = 2
        response = self.app.get('/proximity/{}?k={}'.format(city_id, k))
        self.assert200(response, "valid city ID and k returns 200")
        payload = json.loads(response.data.decode())
        assert payload['limit'] == k
        assert payload['total_available'] == 8
        assert len(payload['cities']) == payload['limit']

        response = self.app.get('/proximity/{}?countryCode=ID'.format(city_id))
        self.assert200(response, "country code not in the database will "
                                 "return 200")
        payload = json.loads(response.data.decode())
        assert payload['limit'] == config.DEFAULT_PROXIMITY_LIMIT
        assert payload['total_available'] == 0
        assert len(payload['cities']) == payload['total_available']

        response = self.app.get('/proximity/{}?countryCode=AD'.format(city_id))
        self.assert200(response, "country code in the database will "
                                 "return 200")
        payload = json.loads(response.data.decode())
        assert payload['limit'] == config.DEFAULT_PROXIMITY_LIMIT
        assert payload['total_available'] == 8
        assert len(payload['cities']) == payload['limit']

        response = self.app.get('/proximity/{}?foo=bar'.format(city_id))
        self.assert400(response, "unsupported parameter should return 400")

        response = self.app.get('/proximity/{}?k=2&foo=bar'.format(city_id))
        self.assert400(response, "extra parameter should return 400")

        response = self.app.get('/proximity/{}?foo=bar&k=2'.format(city_id))
        self.assert400(response, "extra parameter version 2 should return 400")

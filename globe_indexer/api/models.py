# Filename: models.py

"""
Globe Indexer API Models Module

Interface Classes:
    GeoName
"""

# Standard libraries
import datetime
import json

# Globe Indexer
from globe_indexer import db


# pylint: disable=too-few-public-methods
class _BaseModel(db.Model):
    """
    Base Model representation of an entry in the database
    """
    __abstract__ = True

    # pylint: disable=invalid-name
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # pylint: enable=invalid-name

    date_created = db.Column(db.DateTime, nullable=False,
                             default=db.func.current_timestamp())
    date_updated = db.Column(db.DateTime, nullable=True,
                             onupdate=db.func.current_timestmap())
# pylint: enable=too-few-public-methods


# pylint: disable=too-many-instance-attributes,too-few-public-methods
class GeoName(_BaseModel):
    """
    Model representation of a city
    """
    __tablename__ = 'geo_name'

    name = db.Column(db.String(200), nullable=False)
    ascii_name = db.Column(db.String(200), nullable=False)
    alternate_names = db.Column(db.String(255))

    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    feature_class = db.Column(db.CHAR(1))
    feature_code = db.Column(db.String(10))

    country_code = db.Column(db.CHAR(2), nullable=False)
    cc2 = db.Column(db.String(200))

    admin1_code = db.Column(db.String(20))
    admin2_code = db.Column(db.String(80))
    admin3_code = db.Column(db.String(20))
    admin4_code = db.Column(db.String(20))

    population = db.Column(db.BigInteger)
    elevation = db.Column(db.Integer)
    dem = db.Column(db.Integer)

    timezone = db.Column(db.String(40))
    modification_date = db.Column(db.Date)

    def __init__(self, doc):
        """
        Constructor

        :param doc: dictionary-like instance
        """
        # pylint: disable=invalid-name
        self.id = int(doc['geonameid'])
        # pylint: enable=invalid-name

        self.name = doc['name']
        self.ascii_name = doc['asciiname']

        alternate_names = [
            name for name in set(doc['alternatenames'].split(','))
        ]
        if alternate_names:
            self.alternate_names = ','.join(alternate_names)
        else:
            self.alternate_names = None

        self.latitude = float(doc['latitude'])
        self.longitude = float(doc['longitude'])

        if doc['feature_class']:
            self.feature_class = doc['feature_class']
        else:
            self.feature_class = None

        self.feature_code = doc['feature_code'] if doc['feature_code'] else None

        self.country_code = doc['country_code']

        alternate_cc = [
            code for code in doc['cc2'].split(',') if code]
        self.cc2 = ','.join(alternate_cc) if alternate_cc else None

        self.admin1_code = doc['admin1_code'] if doc['admin1_code'] else None
        self.admin2_code = doc['admin2_code'] if doc['admin2_code'] else None
        self.admin3_code = doc['admin3_code'] if doc['admin3_code'] else None
        self.admin4_code = doc['admin4_code'] if doc['admin4_code'] else None

        self.population = int(doc['population']) if doc['population'] else None
        self.elevation = int(doc['elevation']) if doc['elevation'] else None
        self.dem = int(doc['dem']) if doc['dem'] else None

        self.timezone = doc['timezone']

        self.modification_date = datetime.datetime.strptime(
            doc['modification_date'], '%Y-%m-%d').date()

    def __repr__(self):
        """
        Represent the city in a more readable format

        :returns: str
        """
        return '<GeoName {}>'.format(self.id)

    def __eq__(self, other):
        """
        Check if two instances are equal.

        :param other: another instance of :class:`api.models.GeoName`
        :returns: boolean
        """
        return self.id == other.id

    def json(self):
        """
        Represent the city in JSON format

        :returns: JSON object
        """
        value = {
            'id': self.id,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'country_code': self.country_code,
        }
        return json.loads(json.dumps(value))
# pylint: enable=too-many-instance-attributes,too-few-public-methods

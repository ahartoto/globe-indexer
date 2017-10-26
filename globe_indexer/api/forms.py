# Filename: forms.py

"""
Globe Indexer API Forms Module
"""

# Flask WTForm
from flask_wtf import FlaskForm

# WTForm
from wtforms import IntegerField, SelectField, StringField
from wtforms.validators import DataRequired

# Globe Indexer
from globe_indexer.config import DEFAULT_PROXIMITY_LIMIT


# Interface Classes
class ProximityForm(FlaskForm):
    """
    Form to input query parameters for proximity search
    """
    geoname_id = IntegerField('city ID', validators=[DataRequired()])
    query_limit = IntegerField('search limit', validators=[DataRequired()],
                               default=DEFAULT_PROXIMITY_LIMIT)
    country_code = SelectField('country code')


class LexicalForm(FlaskForm):
    """
    Form to input query parameter for lexical search
    """
    name = StringField('city name', validators=[DataRequired()])

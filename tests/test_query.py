# Filename: test_query.py

"""
Test content of the api/query.py
"""

# pytest
import pytest

# Globe Indexer
from globe_indexer.api import query
from globe_indexer.error import GlobeIndexerError

# Test
from . import BaseTest


class TestQuery(BaseTest):
    def test_country_codes(self):
        codes = query.country_code_query()
        assert [('', ''), ('AD', 'AD - Andorra')] == codes

    def test_lexical(self):
        results = query.lexical_query(('El',))
        assert len(results) == 0

        results = query.lexical_query(('El', 'Tarter'))
        assert len(results) == 1
        assert results[0].name == 'El Tarter'

    def test_proximity(self):
        city_id = 3039678
        results = query.proximity_query(city_id)
        assert len(results) == 8

        city_ids = [city[1] for city in results]
        assert city_id not in city_ids

        results = query.proximity_query(city_id, country_code='ID')
        assert len(results) == 0

        with pytest.raises(GlobeIndexerError):
            query.proximity_query(-1)

# Filename: test_utils.py

"""
Test content of the utils.py
"""

# Standard libraries
import os

# Globe Indexer
from globe_indexer import utils


class TestParseGeonameTable:
    @classmethod
    def setup_class(cls):
        cls.input_fpath = os.path.join(os.path.dirname(__file__), 'data',
                                       'geoname_example.txt')

    def test_parse(self):
        rows = utils.parse_geoname_table_file(self.input_fpath)
        assert len(rows) == 9

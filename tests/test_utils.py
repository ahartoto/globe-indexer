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

    def test_parse_input_file(self):
        rows = utils.parse_geoname_table_file(self.input_fpath)
        assert len(rows) == 9


class TestUtils:
    def test_get_query_str(self):
        values = {
            "Las   Vegas": "las%vegas",
            "Paris": "paris",
            "Jak*": "jak%",
            "*Foo* ": "%foo%",
            "**Bar****": "%bar%",
            "A": "a",
            "el dorado": "el%dorado",
        }
        for key, value in values.items():
            words = [word.lower() for word in key.split()]
            assert utils.get_query_string(words) == value

    def test_has_invalid_chars(self):
        for value in ("Jak*", "fooBar", "*", "", "*a*", "*Foo", "***", "Julià"):
            assert utils.has_invalid_chars(value) is False

        for value in ("../..", ".", "123.*123"):
            assert utils.has_invalid_chars(value) is True

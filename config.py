# Filename: config.py

# Standard libraries
import os


class BaseConfig(object):
    """
    Base configuration of the application
    """
    DEBUG = False
    LOG_LEVEL = 'INFO'
    MAIL_FROM_EMAIL = 'ahartoto.dev@gmail.com'
    JSON_AS_ASCII = False
    JSONIFY_MIMETYPE = 'application/json; charset=utf-8'
    JSONIFY_PRETTYPRINT_REGULAR = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///globe_indexer.db'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if os.getenv('APPLICATION_SECRET_KEY') is not None:
        SECRET_KEY = os.getenv('APPLICATION_SECRET_KEY')


class TestConfig(BaseConfig):
    SECRET_KEY = 'TestingSecretKey98765'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    WTF_CSRF_ENABLED = False

[//]: # (Filename: README.md)

[![Build Status](https://travis-ci.org/ahartoto/globe-indexer.svg?branch=master)](https://travis-ci.org/ahartoto/globe-indexer)
[![Documentation Status](https://readthedocs.org/projects/globe-indexer/badge/?version=latest)](http://globe-indexer.readthedocs.io/en/latest/?badge=latest)


# globe-indexer
Indexing the globe is no easy task. I'm grateful that the GeoNames
had already started the process by providing data accessible through this
[page](http://www.geonames.org).

For this project I will only use the data associated with cities with 
population > 1000 or seats of administration division (ca 150.000).
It can be downloaded from this [link](http://download.geonames.org/export/dump/cities1000.zip).

This project is written mostly in Python (with a tiny bit of HTML), and will
showcase how we can use [Flask](http://flask.pocoo.org) and
[Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org) to serve a page
and create a service (RESTful) to help with the following tasks:

1. Lexical Search - Search cities by their names
2. Proximity Search - Find other cities that are closest to a specific one

For more complete documentation about the approach and notes on this project,
please go this [page](http://globe-indexer.readthedocs.io/en/latest/).

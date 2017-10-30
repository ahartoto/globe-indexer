.. Filename: index.rst

#############
Globe Indexer
#############

Globe Indexer is an application written in Python using
`Flask <http://flask.pocoo.org>`_ and
`Flask-SQLAlchemy <http://flask-sqlalchemy.pocoo.org>`_, and it's deployed
using `AWS Elastic Beanstalk <https://aws.amazon.com/elasticbeanstalk/>`_.

This project uses two approaches to serve the needs of finding information
of cities with population > 1000 or seats of administration division
(ca 150.000) as documented below. The data is provided by the
`GeoNames <http://www.geonames.org>`_ and is parsed with the specification
detailed on this `page <http://download.geonames.org/export/dump/>`_.

.. toctree::
   :maxdepth: 2
   :caption: Approaches:

   api
   pages

Summary
=======

Since the data from GeoNames is presented in a specific format with tab as
the delimiter character, I chose to treat the file as if it were a CSV
file (but changing delimiter character to a tab). This allows me to simply use
the `csv <https://docs.python.org/3/library/csv.html>`_ Python standard library
to parse the file.

The parsed information then gets loaded on to an `SQLite <http://www.sqlite
.org>`_ database so it would persist. Features supported in the current
version of the application deals with searching (or querying) and sorting
(based on distance). Therefore, it makes sense to store the information
into a database. The parsing of the file and loading in onto the database will
occur when the application is launched for the first time in a new host machine.

Due to the size of the data file from GeoNames, it is not committed to the
repository of the project. I've set up the code that would automatically
download and unzip the file once it's downloaded if the expected data file
doesn't exist in the specified location and if the database is empty.

I chose to use `Flask <http://flask.pocoo.org>`_ framework as the foundation of
this application because the learning curve is relatively small, and it
allows me to create such prototype and re-iterate quickly.



Architecture Considerations
===========================
Globe Indexer uses `SQLite <http://www.sqlite.org>`_ for its persistent
data access layer (DAL) for simplicity and scalability:

   * minimum setup time since we don't need it to be hosted.
   * each host machine will have its own copy of the database, and it's
     acceptable since we are not supporting write operations (to add new city
     or update to existing ones).
   * unit tests scenarios can easily be created.

The disadvantages of this approach:

   * Possible mismatch of information among host machines if data from
     GeoNames is updated after a few machines were launched prior to the
     update was made, and additional machines have to be created due to
     increase of load.

Another option that was considered is to use
`AWS RDS <https://aws.amazon.com/rds/>`_ (PostgreSQL + PostGIS).
The advantage of doing so is having one "source of truth". Any update needs
to be made to the data only has to be done once.

Distance Calculation Considerations
===================================

Current application uses
`the Haversine Formula <https://en.wikipedia.org/wiki/Haversine_formula>`_ to
calculate distance between two cities given their coordinates. This approach
is simple and good enough (since it is not always accurate).

Another approach is to use PostgreSQL + PostGIS combination (for DAL) to
help with such calculation. PostGIS will provide an accurate answer, and
performing the calculation, sorting, and therefore, returning closest ``k``
cities is a trivial query.

Cloud Deployment
================



Scalability
===========


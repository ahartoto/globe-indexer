.. Filename: index.rst

#############
Globe Indexer
#############

Globe Indexer is an application written in Python 3 using
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

Since the data from GeoNames is presented in a specific format with tab
(``\t``) as the delimiter character, I chose to treat the file as if it were
a CSV file (but changing delimiter character to a tab). This allows me to
simply use the `csv <https://docs.python.org/3/library/csv.html>`_ Python
standard library to parse the file.

The parsed information then gets loaded on to an
`SQLite <http://www.sqlite.org>`_ database so it would persist.
Features supported in the current version of the application deals with
searching (or querying) and sorting (based on distance). Therefore, it makes
sense to store the information into a database. The parsing of the file and
loading it onto the database will occur when the application is launched for
the first time in a new host machine.

Due to the large size of the data file from GeoNames, it is not committed to the
repository of the project. I have set up the code that would automatically
download and unzip the file once it's downloaded if the expected data file
doesn't exist in the specified location and if the database is empty.

I chose to use `Flask <http://flask.pocoo.org>`_ framework as the foundation of
this application because the learning curve is relatively small, and it
allows me to create a prototype and iterate quickly.

A ``GeoName`` model was created to easily represent a record/city in the
database. ``SQLAlchemy`` makes it extremely easy to query the database to
retrieve information of cities based on the query parameter provided to the
application. It also provides high level abstraction that makes it easy if we
ever want to move away from SQLite to other databases such as PostgreSQL.

The rest of the application is mostly about input data validation as well as
presenting the output to the user. Input data validation is required to ensure
that user enters values that are not malicious and valid.

The reason for providing two approaches (RESTful API as well as UI-based) is to
allow other applications or automated processes to query information
using API calls, while the UI-based solution is to provide visualization for
regular users.

.. _arch-section:

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
   * SQLite supports limited level of concurrency.

Another option that was considered is to use
`AWS RDS <https://aws.amazon.com/rds/>`_ (PostgreSQL + PostGIS).
The advantages of this option are:

   * having one "source of truth". Any data update only has to be done once.
   * higher level of concurrency support.

The disadvantages:

   * It costs money to host database using this approach.
   * Additional steps required to install PostGIS on the RDS-PostgreSQL
     instance.
   * Record insertions takes significantly longer than on SQLite even
     with a relatively decent (``m3.large``) instance type.
   * To accommodate for integration testing, it would be necessary to setup
     another RDS-PostgreSQL instance set up.

Distance Calculation Considerations
===================================

Current application uses
`the Haversine Formula <https://en.wikipedia.org/wiki/Haversine_formula>`_ to
calculate distance between two cities given their coordinates. This approach
is simple and good enough (but it is not always accurate).

Another approach is to use PostgreSQL + PostGIS combination (for DAL) to
help with such calculation. PostGIS will provide an accurate answer, and
performing the calculation, sorting, and therefore, returning closest ``k``
cities is a trivial query. However, as mentioned in the :ref:`arch-section`
section, there is cost and other disadvantages of this approach, and team would
have to make a decision on whether such investment will provide enough return.

Cloud Deployment
================

The application is already deployed to the cloud using
`AWS Elastic Beanstalk <https://aws.amazon.com/elasticbeanstalk/>`_. The
challenge was to ensure that the application is compatible with Python 3.4
since AWS is still not supporting the latest Python release. It can also a
little bit tricky to get the configuration right for a first time user.

The alternative is to create a Docker container which will provide greater
flexibility. However, due to limited time, I didn't have the chance to
explore this approach.

Scalability
===========

Since we are deploying this to the cloud using
`AWS Elastic Beanstalk <https://aws.amazon.com/elasticbeanstalk/>`_, we have
the flexibility to update the configuration in a way that will allow us to
scale when we see high load (or based on other criteria).

I am pretty satisfied with the performance of one ``m3.large`` instance which
host the application. I had a chance to load test the application using
``jmeter``: 50 concurrent users (ramp up time is set to be 1 second) performing
the same lexical search with city name set to ``Paris``, and the test is set to
run it in a loop of 5 times.

Repeating the experiment 3 times, I'm seeing the following data:

+------------+--------------+
| Experiment | Failure Rate |
+============+==============+
|     1      |     10.4%    |
+------------+--------------+
|     2      |      0%      |
+------------+--------------+
|     3      |     0.4%     |
+------------+--------------+

As expected, the SQLite cannot handle high volume of requests that well.
Hence, we are seeing the high failure rates. However, trying the same approach
with only 10 concurrent users, the responses were consistent, and the system
was able to handle the requests well even though the response gets slower as
we get higher volume of users performing the searches.

Since we are only expected to support 1 user. I believe the solution is
adequate for that, and would recommend migrating to PostgreSQL if we are
expecting to serve high number of users, want to provide reliable service,
and can afford it.

Code Quality
============
The application has been tested with unit tests, passed lint checker (with
limited waivers), and has a decent (line) code coverage. This combination is
essential to guarantee a successful deployment. A well tested application
build trust and provides great user experience and a reliable service that
others can rely upon.

A sample data was taken out of the original data, and then loaded to a separate
SQLite database to allow us to run the tests and iterate quickly. Positive
and negative test cases were created, and can be found in the repository
where the project is hosted.

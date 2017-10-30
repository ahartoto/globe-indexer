.. Filename: api.rst

###########
RESTful API
###########

Health Check
============

``GET /health``


Lexical Search
==============

``GET /lexical?cityName=<name>``


Proximity Search
================

``GET /proximity/<cityID>[?k=<limit>&countryCode=<code>]``


Search By ID
============

``GET /<cityID>``

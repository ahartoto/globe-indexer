.. Filename: api.rst

###########
RESTful API
###########

These endpoints are created to help with cloud deployment and provide a way
for another program or automated processes to interact with our service.

Health Check
============
Endpoint: ``GET /health``

This endpoint is primarily created as a way to detect the health of the
instances where the application is deployed to.

Expected response:

.. code-block:: javascript

   > GET /health
   {
      "message": "API is available"
   }

.. _lexical-search-api:

Lexical Search
==============
Endpoint: ``GET /lexical?cityName=<name>``

Searching cities by their names. User can use the ``*`` character as a
wildcard as well. For instance:

.. code-block:: javascript

   > GET /lexical?cityName=Jakarta
   {
      "cities": [
         {
            "name": "Jakarta",
            "country_code": "ID",
            "longitude": 106.84513,
            "latitude": -6.21462,
            "id": 1642911
         }
      ],
      "total": 1
   }

   > GET /lexical?cityName=Jak*
   {
      "cities": [
         {
            "name": "Jakobstad",
            "country_code": "FI",
            "longitude": 22.70256,
            "latitude": 63.67486,
            "id": 656130
         },
         ...,
         {
            "name": "Jakarta",
            "country_code": "ID",
            "longitude": 106.84513,
            "latitude": -6.21462,
            "id": 1642911
         },
         ...
      ],
      "total": 15
   }

Proximity Search
================
Endpoint: ``GET /proximity/<cityID>[?k=<limit>&countryCode=<code>]``

This endpoint helps the user to find other cities closest to a specific city.
The ``cityID`` can be retrieved by searching the city by its name. See the
:ref:`lexical-search-api` section for more information on that.

By default if no search limit (``k``) was provided, the API will only return
maximum of 5 cities. User can further limit the search by providing a specific
country code (two-letter ISO country code) if desired.

.. note::

   The performance of this query is pretty slow. On average we are seeing
   about 2 seconds of response time per request.

For example:

.. code-block:: javascript

   > GET /proximity/1642911
   {
      "cities": [
         {
            "city": {
               "country_code": "ID",
               "id": 1649378,
               "latitude": -6.2349,
               "longitude": 106.9896,
               "name": "Bekasi"
            },
            "distance": 16.128046998253062
         },
         {
            "city": {
               "country_code": "ID",
               "id": 8581443,
               "latitude": -6.28862,
               "longitude": 106.71789,
               "name": "South Tangerang"
            },
            "distance": 16.29452750300914
         },
         ...,
      ],
      "limit": 5,
      "total_available": 149654
   }

   > GET /proximity/1642911?k=1
   {
      "cities": [
         {
            "city": {
               "country_code": "ID",
               "id": 1649378,
               "latitude": -6.2349,
               "longitude": 106.9896,
               "name": "Bekasi"
            },
            "distance": 16.128046998253062
         }
      ],
      "limit": 1,
      "total_available": 149654
   }

   > GET /proximity/1642911?k=1&countryCode=FI
   {
      "cities": [
         {
            "city": {
               "country_code": "FI",
               "id": 656709,
               "latitude": 62.67162,
               "longitude": 30.93276,
               "name": "Ilomantsi"
            },
            "distance": 9912.501025701393
         }
      ],
      "limit": 1,
      "total_available": 455
   }


.. note::

   The ``total_available`` field in the latest query is different from the
   previous queries, and that is expected since we are narrowing down the
   results to only cities within that country.

Search By ID
============
Endpoint: ``GET /<cityID>``

The idea of this endpoint is to provide a more complete information about a
city given its ID. For example:

.. code-block:: javascript

   > GET /lexical?cityName=Jakarta
   {
      "alternate_names": [
         "Dzakarta",
         "ਜਕਾਰਤਾ",
         ...,
         "ジャカルタ",
         ...,
      ],
      "name": "Jakarta",
      "ascii_name": "Jakarta",
      "country_code": "ID",
      "longitude": 106.84513,
      "latitude": -6.21462,
      "id": 1642911,
      "population": 8540121
   }

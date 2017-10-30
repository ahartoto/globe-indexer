.. Filename: pages.rst

###############
Using The Forms
###############
The form pages are created to help users to visualize the data that's returned
per query. The map with overlays is created using the
`OpenLayer <http://openlayers.org>`_ API.

Lexical Search
==============
We highly recommend user to start from this page. From this page, user will
be able to search for cities based on their names. As documented on our RESTful
API page (:ref:`lexical-search-api` section), user can also use ``*`` character
as a wildcard.

.. note::

   If multiple words are provided, only cities whose names include those words
   in the same order that's given will be returned.


Proximity Search
================
Proximity search enables the user to find the ``k`` closest cities given a
city ID. The city ID can be retrieved from performing the search by name.

.. note::

   User can also change the search by selecting a specific country from the
   drop down menu. This will return closest cities from that country.

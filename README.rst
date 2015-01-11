sphinxcontrib-openstreetmap
===========================

Summary
-------

Sphinxcontrib-openstreetmap supports to embed OpenSteetMap for
your documentation easily.

Usage
-----

Here is the simple example which shows one marker on the map.

::

   .. openstreetmap:: Example OpenStreetMap
      :id: example_openstreetmap1
      :location: 40.689249,-74.0445
      :renderer: leafletjs

      "Liberty Island, New York, United States", location: 40.689249, -74.0445

This markup generates following map.

.. openstreetmap:: Example OpenStreetMap
   :id: example_openstreetmap1
   :location: 40.689249,-74.0445
   :renderer: leafletjs

   "Liberty Island, New York, United States" location: 40.689249, -74.0445



Syntax
------

Here is the syntax of openstreetmap::

    .. openstreetmap:: LABEL_FOR_MAP
       :id: UNIQUEUE_ID_FOR_DIV_TAG
       :location: LATITUDE_AND_LONGITUDE

       MARKER_1_LATITUDE_AND_LONGITUDE
       ...
       MARKER_N_LATITUDE_AND_LONGITUDE

Required parameters
~~~~~~~~~~~~~~~~~~~

`id`
````

Specify unique id for OpenStreetMap data. This `id` is used for id of `div` tag in HTML.

`location`
``````````

Specify the latitude and the longitude of center point in OpenStreetMap.

Optional parameters
~~~~~~~~~~~~~~~~~~~

`LABEL_FOR_MAP`
```````````````

Specify the label for OpenStreetMap data. This label is shown in right bottom of OpenStreetMap.

`renderer`
``````````

Specify the renderer. Currently `reafletjs` is supported.

`MARKER_X_LATITUDE_AND_LONGITUDE`
`````````````````````````````````

`MARKER_X_LATITUDE_AND_LONGITUDE` must be following syntax::


    LABEL_TEXT, location: LATITUDE, LONGITUDE

Here is the simple example of marker::

    "Liberty Island, New York, United States", location: 40.689249, -74.0445






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

   "Liberty Island, New York, United States", location: 40.689249, -74.0445



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

``id``
``````

Specify unique id for map. This `id` is used for ``id`` of ``div`` tag in HTML.

``location``
````````````

Specify the latitude and the longitude of center point in map.

Optional parameters
~~~~~~~~~~~~~~~~~~~

``renderer``
````````````

The default value is ``leafletjs``.

Specify the renderer. Currently only ``leafletjs`` is supported.

``zoom``
````````

The default value is 15.

Specify the value of zoom level.
The value of zoom level must be in 0 to 19.
See `Zoom levels <http://wiki.openstreetmap.org/wiki/Zoom_levels>`_.

``zoomcontrol``
```````````````

The default value is ``true``.

Specify ``false`` if you want to disable zoom feature.

``offline``
```````````

The default value is ``false``.

Specify ``true`` if you want to generate offline map.
Note that offline map doesn't have fully support for zoom feature, so disable zoom feature to set ``false`` for ``zoomcontrol``.

`LABEL_FOR_MAP`
```````````````

Specify the label for map. This label is shown in right bottom of map.

`MARKER_X_LATITUDE_AND_LONGITUDE`
`````````````````````````````````

`MARKER_X_LATITUDE_AND_LONGITUDE` must be following syntax::


    LABEL_TEXT, location: LATITUDE, LONGITUDE

Here is the simple example of marker::

    "Liberty Island, New York, United States", location: 40.689249, -74.0445






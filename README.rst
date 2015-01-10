sphinxcontrib-openstreetmap
===========================

Summary
-------

Sphinxcontrib-openstreetmap supports to embed OpenSteetMap for
your documentation easily.

Usage
-----

Here is the simple example which shows one marker on the map.

.. openstreetmap::
   :id: example_openstreetmap1
   :label: Example OpenStreetMap
   :latitude: 40.689249
   :longitude: -74.0445
   :renderer: leafletjs

   label: "Liberty Island, New York, United States" latitude: 40.689249 longitude: -74.0445

..
   .. openstreetmap::
      :id: example_openstreetmap1
      :label: Example OpenStreetMap
      :latitude: 40.689249
      :longitude: -74.0445
      :renderer: leafletjs

      label: "Liberty Island, New York, United States", latitude: 40.689249, longitude: -74.0445


Syntax
------

Here is the syntax of openstreetmap::

    .. openstreetmap:
       :id: UNIQUEUE_ID_FOR_DIV_TAG
       :label: LABEL_FOR_MAP
       :latitude: LATITUDE
       :longitude: LONGITUDE
       :renderer: leafletjs

       MARKER_1_LATITUDE_AND_LONGITUDE
       ...
       MARKER_N_LATITUDE_AND_LONGITUDE

Required parameters
~~~~~~~~~~~~~~~~~~~

`id`
````

Specify unique id for OpenStreetMap data. This `id` is used for id of `div` tag in HTML.

`label`
```````

Specify the label for OpenStreetMap data. This `label` is shown in right bottom of OpenStreetMap.

`latitude`
``````````

Specify the latitude of center point in OpenStreetMap.

`longitude`
```````````

Specify the longitude of center point in OpenStreetMap.

`renderer`
``````````

Specify the renderer. Currently `reafletjs` is supported.

Optional parameters
~~~~~~~~~~~~~~~~~~~

`MARKER_X_LATITUDE_AND_LONGITUDE`
`````````````````````````````````

`MARKER_X_LATITUDE_AND_LONGITUDE` must be following syntax::


    label: LABEL_TEXT, latitude: LATITUDE, longitude: LONGITUDE

Here is the simple example of marker::

    label: "Liberty Island, New York, United States", latitude: 40.689249, longitude: -74.0445






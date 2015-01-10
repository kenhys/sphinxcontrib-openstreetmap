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

Specify unique id for OpenStreetMap data.

`label`
```````

Specify the label for OpenStreetMap data.

`marker`
````````

Specify unique id for each OpenStreetMap data.

Optional parameters
~~~~~~~~~~~~~~~~~~~

`area`
``````





Summary
-------

Sphinxcontrib-openstreetmap supports to embed OpenSteetMap for
your documentation easily.

Usage
-----

.. openstreetmap::
   :id: example_openstreetmap1
   :label: Example OpenStreetMap
   :longitude: 139.00
   :latitude: 35.40

   {'id': 1, 'label': 'hoge', 'longitude': 139.50, 'latitude': 35.40}
   {'id': 2, 'label': 'hoge', 'longitude': 139.00, 'latitude': 35.40}

.. openstreetmap::
   :id: example_openstreetmap2
   :label: Example OpenStreetMap
   :longitude: 139.00
   :latitude: 35.40

   {'id': 1, 'label': 'hoge', 'longitude': 139.25, 'latitude': 35.40}


Syntax
------

Here is the syntax of openstreetmap::

    .. openstreetmap:
       :id: UNIQUEUE_ID_FOR_OPENSTREETMAP
       :label: LABEL_FOR_OPENSTREETMAP
       :marker: {'longitude': 1111, 'latitude': 2222}

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





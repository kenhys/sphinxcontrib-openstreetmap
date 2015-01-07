# -*- coding: utf-8 -*-
"""
	sphinxcontrib.openstreetmap
	===========================

	Embed OpenStreetMap on your documentation.

	:copyright: Copyright 2015 HAYASHI Kentaro <kenhys@gmail.com>
	:license: BSD, see LICENSE for details.
"""
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive

class openstreetmap(nodes.General, nodes.Element):
    pass

class OpenStreetMapDirective(Directive):
    """Directive for embedding OpenStreetMap"""
    has_content = True
    option_spec = {
        'id': directives.unchanged,
        'label': directives.unchanged,
        'latitude': directives.unchanged,
        'longitude': directives.unchanged,
    }

    def run(self):
        node = openstreetmap()
        if 'id' in self.options:
            node['id'] = self.options['id']
        else:
            msg = ('openstreetmap directive needs uniqueue id for map data')
            return [document.reporter.warning(msg, line=self.lineno)]
        points = []
        for line in self.content:
            point = eval(line)
            points.append(point)
        node['marker'] = points
        node['view'] = {
            'longitude': self.options['longitude'],
            'latitude': self.options['latitude']
        }
        print(points)
        return [node]

def visit_openstreetmap_node(self, node):
    map_id = node['id']
    markers = node['marker']
    longitude = node['view']['longitude']
    latitude = node['view']['latitude']
    self.body.append("""
    <link rel='stylesheet' href='http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.css'/>
    <script src='http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.js'></script>
    <div id='%s' style='height: auto !important; height: 100%%; min-height: %s;'>
    <script type='text/javascript'>
        var map = L.map('%s').setView([%s, %s], 11);
        var tileLayer = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                                    attribution : '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);
    """ % (map_id, '400px', map_id, latitude, longitude))
    self.body.append("""
    var markers = [
    """)
    for marker in markers:
        self.body.append("""
        {latitude: %s, longitude: %s},
        """ % (marker['latitude'], marker['longitude']))
    self.body.append("""
    ];
    """)
    self.body.append("""
    for (var i = 0; i < markers.length; i++) {
      var marker = markers[i];
      var mapMarker = L.marker([marker['latitude'], marker['longitude']], {title: 'aaaa'});
      mapMarker.addTo(map);
      mapMarker.bindPopup('Popup sample');
      mapMarker.openPopup();
    }
    """)
    self.body.append("""
        L.control.scale().addTo(map);
      </script>
    </div>
    """)

def depart_openstreetmap_node(self, node):
    pass

def setup(app):
    app.add_node(openstreetmap,
                 html=(visit_openstreetmap_node, depart_openstreetmap_node))
    app.add_directive('openstreetmap', OpenStreetMapDirective)


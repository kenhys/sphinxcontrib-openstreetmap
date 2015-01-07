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


class OpenStreetMapRenderer:
    pass


class OpenStreetMapLeafletjsRenderer(OpenStreetMapRenderer):
    pass


class openstreetmap(nodes.General, nodes.Element):
    pass


class OpenStreetMapDirective(Directive):
    """Directive for embedding OpenStreetMap"""
    has_content = True
    option_spec = {
        'id': directives.unchanged,
        'label': directives.unchanged,
        'renderer': directives.unchanged,
        'latitude': directives.unchanged,
        'longitude': directives.unchanged,
    }

    def __milliseconds_to_degree(self, value):
        return value / 3600000

    def __convert_to_hash(self, line):
        hash = {}
        for item in line.split(','):
            pre, post = item.split(':')
            key = pre.strip()
            value = post.strip()
            if key == "label":
                hash[key] = value
            elif key == "longitude" or key == "latitude":
                milliseconds = eval(value)
                if isinstance(milliseconds, float):
                    hash[key] = milliseconds
                else:
                    self.__milliseconds_to_degree(milliseconds)
            else:
                hash[key] = value
        return hash

    def is_valid_renderer(self, renderer):
        if renderer in ['leafletjs']:
            return True
        else:
            return False

    def run(self):
        node = openstreetmap()
        if 'id' in self.options:
            node['id'] = self.options['id']
        else:
            msg = ('openstreetmap directive needs uniqueue id for map data')
            return [document.reporter.warning(msg, line=self.lineno)]

        if 'renderer' in self.options:
            if self.is_valid_renderer(self.options['renderer']):
                node['renderer'] = self.options['renderer']
            else:
                msg = ('renderer: %s is not valid.' % renderer['renderer'])
                return [document.reporter.warning(msg, line=self.lineno)]
        else:
            node['renderer'] = 'leafletjs'

        points = []
        for line in self.content:
            point = self.__convert_to_hash(line)
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

    renderer = None
    if node['renderer'] == "leafletjs":
        renderer = OpenStreetMapLeafletjsRenderer()
    else:
        msg = ('renderer: %s is not supported.' % renderer['renderer'])
        return [document.reporter.warning(msg, line=self.lineno)]

    renderer.render(node)

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

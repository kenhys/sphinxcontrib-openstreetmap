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
import shlex

class OpenStreetMapRenderer(object):
    pass


class OpenStreetMapLeafletjsRenderer(OpenStreetMapRenderer):
    def __init__(self):
        super(OpenStreetMapRenderer, self).__init__()

    def __header__(self):
        cdn_url = "http://cdn.rawgit.com/Leaflet/Leaflet.label/master"

        body = """
        <link rel="stylesheet" href="%(cdn)s/libs/leaflet/leaflet.css" />
        <!--[if lte IE 8]>
        <link rel="stylesheet" href="%(cdn)s/libs/leaflet/leaflet.ie.css" />
        <![endif]-->
        <link rel="stylesheet" href="%(cdn)s/dist/leaflet.label.css" />
        <script src="%(cdn)s/libs/leaflet/leaflet-src.js"></script>
        <script src="%(cdn)s/src/Label.js"></script>
        <script src="%(cdn)s/src/BaseMarkerMethods.js"></script>
        <script src="%(cdn)s/src/Marker.Label.js"></script>
        <script src="%(cdn)s/src/CircleMarker.Label.js"></script>
        <script src="%(cdn)s/src/Path.Label.js"></script>
        <script src="%(cdn)s/src/Map.Label.js"></script>
        <script src="%(cdn)s/src/FeatureGroup.Label.js"></script>
        """ % {"cdn": cdn_url}
        return body

    def render(self, node):
        map_id = node['id']
        label = node['label']
        longitude = node['view']['longitude']
        latitude = node['view']['latitude']
        zoom = node['zoom']

        params = {
            "map_id": map_id,
            "label": label,
            "height": "400px",
            "latitude": latitude,
            "longitude": longitude,
            "zoom": zoom,
            "osm_link": "<a href='http://openstreetmap.org'>OpenStreetMap</a>"
        }
        body = ""
        body += self.__header__()
        body += """
        <div id='%(map_id)s' style='width: 100%%; height: %(height)s;'>
        <script type='text/javascript'>
        var osm_url = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
        var attr = "%(label)s | Map data &copy; %(osm_link)s contributors";
        var osm = new L.TileLayer(osm_url, {attribution: attr});
        var latlng = new L.LatLng(%(latitude)s, %(longitude)s);
        var %(map_id)s = new L.Map('%(map_id)s',
                                   {layers: [osm],
                                    center: latlng,
                                    zoom: %(zoom)d});
        """ % params
        markers = node['marker']

        body += "var markers = ["
        for marker in markers:
            body += """
            {label: "%s", latitude: %s, longitude: %s},
            """ % (marker['label'], marker['latitude'], marker['longitude'])
        body += "];"
        body += """
        for (var i = 0; i < markers.length; i++) {
          var marker = markers[i];
          var latlng = [marker['latitude'], marker['longitude']];
          var label = marker['label'];
          L.marker(latlng).bindLabel(label, {noHide: true}).addTo(%s);
        }
        """ % map_id
        body += "</script>"
        body += "</div>"
        return body


class openstreetmap(nodes.General, nodes.Element):
    pass


class OpenStreetMapDirective(Directive):
    """Directive for embedding OpenStreetMap"""
    has_content = True
    key_is_even = True
    required_arguments = 0
    optional_arguments = 32
    option_spec = {
        'id': directives.unchanged,
        'renderer': directives.unchanged,
        'latitude': directives.unchanged,
        'longitude': directives.unchanged,
        'zoom': directives.unchanged,
    }

    def __milliseconds_to_degree(self, value):
        return value / 3600000

    def __is_key_index(self, index):
        mod = 0
        if self.key_is_even:
            mod = 0
        else:
            mod = 1

        if index % 2 == mod:
            return True
        else:
            return False

    def __is_label_text(self, text, index):
        if index != 0:
            return False
        if text in ["longitude:", "latitude:", "label:"]:
            return False
        else:
            return True

    def __convert_to_hash(self, line):
        hash = {}
        items = shlex.split(line)
        index = 0
        key = ""
        value = ""
        self.key_is_even = True
        for item in shlex.split(line):
            if self.__is_key_index(index):
                if self.__is_label_text(item, index):
                    hash["label"] = item
                    self.key_is_even = False
                else:
                    key = item.replace(":", "")
            else:
                if item.endswith(","):
                    value = item[0:-1]
                else:
                    value = item
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
            index = index + 1
        return hash

    def is_valid_renderer(self, renderer):
        if renderer in ['leafletjs']:
            return True
        else:
            return False

    def run(self):
        node = openstreetmap()
        document = self.state.document
        if 'id' in self.options:
            node['id'] = self.options['id']
        else:
            msg = ('openstreetmap directive needs uniqueue id for map data')
            return [document.reporter.warning(msg, line=self.lineno)]

        if self.arguments == []:
            msg = ('openstreetmap directive needs label for map')
            return [document.reporter.warning(msg, line=self.lineno)]
        else:
            node['label'] = "".join(self.arguments)

        if 'renderer' in self.options:
            if self.is_valid_renderer(self.options['renderer']):
                node['renderer'] = self.options['renderer']
            else:
                msg = ('renderer: %s is not valid.' % renderer['renderer'])
                return [document.reporter.warning(msg, line=self.lineno)]
        else:
            node['renderer'] = 'leafletjs'

        if 'zoom' in self.options:
            node['zoom'] = eval(self.options['zoom'])
        else:
            node['zoom'] = 15

        points = []
        for line in self.content:
            point = self.__convert_to_hash(line)
            points.append(point)
        node['marker'] = points
        node['view'] = {
            'longitude': self.options['longitude'],
            'latitude': self.options['latitude']
        }
        return [node]


def visit_openstreetmap_node(self, node):
    renderer = None
    if node['renderer'] == "leafletjs":
        renderer = OpenStreetMapLeafletjsRenderer()
    else:
        msg = ('renderer: %s is not supported.' % renderer['renderer'])
        return [document.reporter.warning(msg, line=self.lineno)]

    self.body.append(renderer.render(node))


def depart_openstreetmap_node(self, node):
    pass


def setup(app):
    app.add_node(openstreetmap,
                 html=(visit_openstreetmap_node, depart_openstreetmap_node))
    app.add_directive('openstreetmap', OpenStreetMapDirective)

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
        latitude = node['location'][0]
        longitude = node['location'][1]
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
            """ % (marker['label'], marker['location'][0], marker['location'][1])
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
        'location': directives.unchanged,
        'zoom': directives.unchanged,
    }

    def __milliseconds_to_degree(self, value):
        return value / 3600000.0

    def __is_key_index(self, state, index):
        mod = 0
        if state['key_is_even']:
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
        if text in ["location:", "label:"]:
            return False
        else:
            return True

    def parse_location_context(self, state):
        index = state['index']
        items = state['items']
        lat = latitude = None
        lng = longitude = None
        if index + 1 < len(items):
            if self.is_latitude_x_longitude(items[index + 1]):
                lat, lng = items[index + 1].split("x")
                index = index + 1
            else:
                if items[index + 1].endswith(","):
                    lat = items[index + 1][0:-1]
                    lng = items[index + 2]
                    index = index + 2
                    if state['key_is_even']:
                        state['key_is_even'] = False
                    else:
                        state['key_is_even'] = True
                else:
                    lat, lng = items[index + 1].split(",")
                    index = index + 1
            latitude = self.parse_latlng(lat)
            longitude = self.parse_latlng(lng)
        else:
            raise ValueError("location value is invalid: %s" % items[index + 1])
        state['index'] = index
        return [latitude, longitude]

    def parse_rectangle_context(self, state):
        index = state['index']
        items = state['items']
        top_left_lat = None
        top_left_lng = None
        bottom_right_lat = None
        bottom_right_lng = None
        top_right_lat = None
        top_right_lng = None
        bottom_left_lat = None
        bottom_left_lng = None
        if index + 1 < len(items):
            lat1, lng1, lat2, lng2 = items[index + 1].split(",")
            top_left_lat = self.parse_latlng(lat1)
            top_left_lng = self.parse_latlng(lng1)
            bottom_right_lat = self.parse_latlng(lat2)
            bottom_right_lng = self.parse_latlng(lng2)
            top_right_lat = top_left_lat
            top_right_lng = bottom_right_lng
            bottom_left_lat = bottom_right_lat
            bottom_left_lng = top_left_lng

        return [[top_left_lat, top_left_lng],
                [top_right_lat, top_right_lng],
                [bottom_right_lat, bottom_right_lng],
                [bottom_left_lat, bottom_left_lng],
                [top_left_lat, top_left_lng]]

    def __convert_to_hash(self, line):
        hash = {}
        index = 0
        key = ""
        value = ""
        items = shlex.split(line)
        state = {
            'key_is_even': True,
            'index': 0,
            'items': items
        }
        while state['index'] < len(items):
            index = state['index']
            item = items[index]
            if self.__is_key_index(state, index):
                if self.__is_label_text(item, index):
                    hash["label"] = item
                    state['key_is_even'] = False
                elif item == "location:":
                    hash["location"] = self.parse_location_context(state)
                elif item == "rectangle:":
                    hash["rectangle"] = self.parse_rectangle_context(state)
                else:
                    key = item[0:-1]
            else:
                if item.endswith(","):
                    value = item[0:-1]
                else:
                    value = item
                hash[key] = value
            state['index'] = state['index'] + 1
        return hash

    def is_milliseconds(self, value):
        if isinstance(value, float):
            return False
        else:
            return True

    def is_latitude_x_longitude(self, text):
        if text.find("x") > 0:
            return True
        else:
            return False

    def parse_latlng(self, text):
        value = eval(text)
        if self.is_milliseconds(value):
            latlng = self.__milliseconds_to_degree(value)
        else:
            latlng = eval(text)
        return latlng

    def parse_location(self, location):
        latitude = None
        longitude = None

        if location.find(',') > 0:
            lat, lng = location.split(',')
        elif location.find('x') > 0:
            lat, lng = location.split('x')
        else:
            raise ValueError("invalid location: %s" % location)

        latitude = self.parse_latlng(lat)
        longitude = self.parse_latlng(lng)

        return [latitude, longitude]

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
            msg = ("label isn't specified for openstreetmap directive")
            document.reporter.warning(msg, line=self.lineno)
            node['label'] = "Example"
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
        rectangles = []
        for line in self.content:
            point = self.__convert_to_hash(line)
            if "rectangle" in point:
                rectangles.append(point)
            else:
                points.append(point)
        node['marker'] = points
        node['rectangle'] = rectangles

        node['location'] = [None,None]
        if 'location' in self.options:
            try:
                node['location'] = self.parse_location(self.options['location'])
            except ValueError:
                msg = ('location value is invalid: %s'
                       'Use LATITUDE,LONGITUDE or LATITUDExLONGITUDE format'
                       % self.options['location'])
                return [document.reporter.error(msg, line=self.lineno)]
        else:
            msg = ("location isn't specified for openstreetmap directive")
            return [document.reporter.error(msg, line=self.lineno)]
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

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
import csv
import math
import os
import urllib


def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - 
                 math.log(math.tan(lat_rad) +
                          (1 / math.cos(lat_rad))) /
                 math.pi) / 2.0 * n)
    return (xtile, ytile)

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

    def generate_rectangle_script(self, map_id, data):
        body = "L.multiPolygon(["
        label = ""
        for rect in data:
            body += "["
            label = rect['label']
            for pair in rect['rectangle']:
                body += "[%s, %s]," % (pair[0], pair[1])
            body += "]"
        body += """
        ]).bindLabel("%s").addTo(%s);""" % (label, map_id)
        return body

    def generate_circle_script(self, map_id, data):
        body = ""
        for circle in data:
            label = circle['label']
            items = circle['circle']
            latitude = items['latitude']
            longitude = items['longitude']
            radius = items['radius']
            body += """
            L.circle([%s, %s], %d).bindLabel("%s").addTo(%s);
            """ % (latitude, longitude, radius, label, map_id)
        return body

    def fetch_leafletjs(self, translator):
        cdn_url = "http://cdn.rawgit.com/Leaflet/Leaflet.label/master"
        outdir = translator.builder.outdir
        prefix = "_static"

        base = "%s/%s/leafletjs" % (outdir, prefix)

        files = [
            "libs/leaflet/leaflet.css",
            "libs/leaflet/leaflet.ie.css",
            "dist/leaflet.label.css",
            "libs/leaflet/leaflet-src.js",
            "src/Label.js",
            "src/BaseMarkerMethods.js",
            "src/Marker.Label.js",
            "src/CircleMarker.Label.js",
            "src/Path.Label.js",
            "src/Map.Label.js",
            "src/FeatureGroup.Label.js",
        ]

        for name in files:
            src = "%s/%s" % (cdn_url, name)
            dest = "%s/%s" % (base, os.path.basename(name))
            if not os.path.exists(os.path.dirname(dest)):
                os.makedirs(os.path.dirname(dest))
            if not os.path.exists(dest):
                urllib.urlretrieve(src, dest)

    def fetch_tile_images(self, prefix, latitude, longitude, zoom):
        lat_num, lng_num = deg2num(latitude, longitude, zoom)
        for x in range(-2, 3):
            for y in range(-2, 3):
                base = "http://a.tile.openstreetmap.org"
                image_path = "%d/%d/%d.png" % (zoom, lat_num + x, lng_num + y)
                image_url = "%s/%s" % (base, image_path)
                path = "%s/_static/tiles/%s" % (prefix, image_path)
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))
                if not os.path.exists(path):
                    urllib.urlretrieve(image_url, path)

    def generate_relative_prefix(self, translator):
        docname = translator.builder.current_name
        prefix = ""
        for name in docname.split("/"):
            if name != docname:
                prefix = "../" + prefix
        return prefix

    def render(self, translator, node):
        map_id = node['id']
        label = node['label']
        latitude = node['location'][0]
        longitude = node['location'][1]
        zoom = node['zoom']
        zoomcontrol = node['zoomcontrol']

        params = {
            "map_id": map_id,
            "label": label,
            "height": "400px",
            "latitude": latitude,
            "longitude": longitude,
            "zoom": zoom,
            "zoomControl": zoomcontrol,
            "osm_link": "<a href='http://openstreetmap.org'>OpenStreetMap</a>"
        }
        if zoomcontrol == "false":
            params['minZoom'] = zoom
            params['maxZoom'] = zoom

        body = ""
        body += self.__header__()
        body += """
        <div id='%(map_id)s' style='width: 100%%; height: %(height)s;'>
        <script type='text/javascript'>
        """ % params

        prefix = ""
        if node['offline']:
            prepend = self.generate_relative_prefix(translator)
            prefix = prepend + "_static/tiles"
            self.fetch_tile_images(translator.builder.outdir,
                                   latitude, longitude, zoom)
            self.fetch_leafletjs(translator)
        else:
            prefix = "http://{s}.tile.openstreetmap.org"
        body += "var osm_url = '%s/{z}/{x}/{y}.png';" % prefix

        body += """
        var attr = "%(label)s | Map data &copy; %(osm_link)s contributors";
        var osm = new L.TileLayer(osm_url, {attribution: attr});
        var latlng = new L.LatLng(%(latitude)s, %(longitude)s);
        var %(map_id)s = new L.Map('%(map_id)s', {""" % params

        body += """
        layers: [osm],
        center: latlng,
        zoom: %(zoom)d,
        zoomControl: %(zoomControl)s,
        """ % params
        if zoomcontrol == "false":
            body += """
            minZoom: %(minZoom)d,
            maxZoom: %(maxZoom)d,
            """ % params
        body += "});"

        markers = node['marker']

        body += "var markers = ["
        for marker in markers:
            latitude = marker['location'][0]
            longitude = marker['location'][1]
            body += """
            {label: "%s", latitude: %s, longitude: %s},
            """ % (marker['label'], latitude, longitude)
        body += "];"
        body += """
        for (var i = 0; i < markers.length; i++) {
          var marker = markers[i];
          var latlng = [marker['latitude'], marker['longitude']];
          var label = marker['label'];
          L.marker(latlng).bindLabel(label, {noHide: true}).addTo(%s);
        }
        """ % map_id
        body += self.generate_rectangle_script(map_id, node['rectangle'])
        body += self.generate_circle_script(map_id, node['circle'])
        body += "</script>"
        body += "</div>"
        return body


class openstreetmap(nodes.General, nodes.Element):
    pass


class OpenStreetMapDirective(Directive):
    """Directive for embedding OpenStreetMap"""
    has_content = True
    key_is_even = True
    offline = False
    required_arguments = 0
    optional_arguments = 32
    option_spec = {
        'id': directives.unchanged,
        'renderer': directives.unchanged,
        'location': directives.unchanged,
        'zoom': directives.unchanged,
        'zoomcontrol': directives.unchanged,
        'offline': directives.unchanged,
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
        lat = None
        lng = None
        if self.is_latitude_x_longitude(items[index]):
            loc, value = items[index].split(":")
            lat, lng = value.split("x")
        else:
            lat = items[index].split(":")[1]
            lng = items[index + 1]
            state['index'] = index + 1
        latitude = self.parse_latlng(lat)
        longitude = self.parse_latlng(lng)
        return [latitude, longitude]

    def parse_rectangle_context(self, state):
        index = state['index']
        items = state['items']

        lat1 = items[index].split(":")[1]
        lng1 = items[index + 1]
        lat2 = items[index + 2]
        lng2 = items[index + 3]

        top_left_lat = self.parse_latlng(lat1)
        top_left_lng = self.parse_latlng(lng1)
        bottom_right_lat = self.parse_latlng(lat2)
        bottom_right_lng = self.parse_latlng(lng2)
        top_right_lat = top_left_lat
        top_right_lng = bottom_right_lng
        bottom_left_lat = bottom_right_lat
        bottom_left_lng = top_left_lng

        state['index'] = index + 3
        return [[top_left_lat, top_left_lng],
                [top_right_lat, top_right_lng],
                [bottom_right_lat, bottom_right_lng],
                [bottom_left_lat, bottom_left_lng],
                [top_left_lat, top_left_lng]]

    def parse_circle_context(self, state):
        index = state['index']
        items = state['items']

        if self.is_latitude_x_longitude(items[index]):
            loc, value = items[index].split(":")
            lat, lng = value.split("x")
        else:
            lat = items[index].split(":")[1]
            lng = items[index + 1]
            state['index'] = index + 1
        latitude = self.parse_latlng(lat)
        longitude = self.parse_latlng(lng)
        radius = 500

        return {'latitude': latitude,
                'longitude': longitude,
                'radius': radius}

    def __convert_to_hash(self, line):
        hash = {}
        index = 0
        key = ""
        value = ""
        state = {
            'key_is_even': True,
            'index': 0,
        }
        for row in csv.reader([line], delimiter=","):
            items = row
            state['items'] = row
        while state['index'] < len(items):
            index = state['index']
            item = items[index]
            if self.__is_key_index(state, index):
                if self.__is_label_text(item, index):
                    hash["label"] = item.decode("utf-8")
                    state['key_is_even'] = False
                elif item.find("location:") > 0:
                    hash["location"] = self.parse_location_context(state)
                elif item.find("rectangle:") > 0:
                    hash["rectangle"] = self.parse_rectangle_context(state)
                elif item.find("circle:") > 0:
                    hash["circle"] = self.parse_circle_context(state)
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
            node['label'] = " ".join(self.arguments)

        if 'renderer' in self.options:
            if self.is_valid_renderer(self.options['renderer']):
                node['renderer'] = self.options['renderer']
            else:
                msg = ('renderer: %s is not valid.' % self.options['renderer'])
                return [document.reporter.warning(msg, line=self.lineno)]
        else:
            node['renderer'] = 'leafletjs'

        if 'zoom' in self.options:
            node['zoom'] = eval(self.options['zoom'])
        else:
            node['zoom'] = 15

        if 'zoomcontrol' in self.options:
            node['zoomcontrol'] = self.options['zoomcontrol']
        else:
            node['zoomcontrol'] = "true"

        if 'offline' in self.options:
            if "true" == self.options['offline']:
                self.offline = True
            elif "false" == self.options['offline']:
                self.offline = False
        node['offline'] = self.offline

        points = []
        rectangles = []
        circles = []
        for line in self.content:
            point = self.__convert_to_hash(line.encode("utf-8"))
            if 'rectangle' in point.keys():
                rectangles.append(point)
            elif 'circle' in point.keys():
                circles.append(point)
            else:
                points.append(point)
        node['marker'] = points
        node['rectangle'] = rectangles
        node['circle'] = circles

        node['location'] = [None, None]
        if 'location' in self.options:
            try:
                location = self.options['location']
                node['location'] = self.parse_location(location)
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
    document = self.document
    if node['renderer'] == "leafletjs":
        renderer = OpenStreetMapLeafletjsRenderer()
    else:
        msg = ('renderer: %s is not supported.' % renderer['renderer'])
        return [document.reporter.warning(msg, line=self.lineno)]

    self.body.append(renderer.render(self, node))


def depart_openstreetmap_node(self, node):
    pass


def setup(app):
    app.add_node(openstreetmap,
                 html=(visit_openstreetmap_node, depart_openstreetmap_node))
    app.add_directive('openstreetmap', OpenStreetMapDirective)

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


class OpenStreetMapRenderer(object):
    pass


class OpenStreetMapLeafletjsRenderer(OpenStreetMapRenderer):
    def __init__(self):
        super(OpenStreetMapRenderer, self).__init__()

    def __header__(self):
        cdn_url = "http://cdn.leafletjs.com/leaflet-0.7.3"

        body = ""
        body += "<link ref='stylesheet' href='%s/leaflet.css'/>" % cdn_url
        body += "<script src='%s/leaflet.js'></script>" % cdn_url
        return body

    def render(self, node):
        map_id = node['id']
        longitude = node['view']['longitude']
        latitude = node['view']['latitude']

        body = ""
        body += self.__header__()
        body += "<div id='%s' style='min-height: %s;'>" % (map_id, '400px')
        body += "<script type='text/javascript'>"

        body += "var osm_url = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';"
        body += "var attr = 'Map data &copy; <a href=http://openstreetmap.org>OpenStreetMap</a> contributors';"
        body += "var %s = new L.map('%s').setView([%s, %s], 13);" % (map_id, map_id, latitude, longitude)
        body += "var osm = new L.tileLayer(osm_url, {attribution: attr}).addTo(%s);" % map_id

        markers = node['marker']
        body += "var markers = ["
        for marker in markers:
            body += "{latitude: %s, longitude: %s}," % (marker['latitude'], marker['longitude'])


        body += "];"
        body += """
        for (var i = 0; i < markers.length; i++) {
        var marker = markers[i];
        var mapMarker = L.marker([marker['latitude'], marker['longitude']], {title: 'aaaa'});
        mapMarker.addTo(%s);
        mapMarker.bindPopup('Popup sample');
        mapMarker.openPopup();
        }
        """ % map_id
        body += "L.control.scale().addTo(%s);" % map_id

        body += "</script>"
        body += "</div>"
        print("BODY: %s" % body)
        return body


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

    self.body.append(renderer.render(node))

def depart_openstreetmap_node(self, node):
    pass


def setup(app):
    app.add_node(openstreetmap,
                 html=(visit_openstreetmap_node, depart_openstreetmap_node))
    app.add_directive('openstreetmap', OpenStreetMapDirective)

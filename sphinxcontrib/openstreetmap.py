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
    has_content = False
    option_spec = {
        'id': directives.unchanged,
        'label': directives.unchanged,
    }

    def run(self):
        node = openstreetmap()
        if 'id' in self.options:
            node['id'] = self.options['id']
        else:
            msg = ('openstreetmap directive needs uniqueue id for map data')
            return [document.reporter.warning(msg, line=self.lineno)]
        return [node]

def visit_openstreetmap_node(self, node):
    self.body.append("<div id='openstreetmap' style='color:red'>OpenStreetMap directive</div>")

def depart_openstreetmap_node(self, node):
    pass

def setup(app):
    app.add_node(openstreetmap,
                 html=(visit_openstreetmap_node, depart_openstreetmap_node))
    app.add_directive('openstreetmap', OpenStreetMapDirective)


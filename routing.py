#!/usr/bin/python
# -*- encoding: utf-8 -*-
from server.controller.home.IndexView import HomeIndex

CONFIG = {
    'ENCODING': 'utf-8'
}

_app = None


def init_routing(app):
    print 'init app in routing'

    app.add_url_rule('/', view_func=HomeIndex.as_view('index', template_name='index.html'))


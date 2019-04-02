#!/usr/bin/python
# -*- encoding: utf-8 -*-
CONFIG = {
    'ENCODING': 'utf-8'
}

_app = None


def init_app(app):
    print 'init app in template_filter'
    if not app:
        return

    if 'ENCODING' in app.config:
        CONFIG['ENCODING'] = app.config['ENCODING']

    global _app
    _app = app
    from . import common_filter

def get_app():
    return _app
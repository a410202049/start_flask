#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

v2 = None


def init_api(api):

    if not api:
        raise RuntimeError('api is None')

    global v2
    v2 = api.namespace('v2', description='version')
    api.version = 'v2'

    @api.errorhandler
    def default_error_handler(error):
        return {'message': str(error)}, getattr(error, 'code', 500)

    __import__('server.controller.resource.user')





#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import time

from flask import Response, jsonify
import json
from flask_restplus import Resource

from server.exception import SUCCESS
import requests


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

    __import__('server.controller.resource.account')


class BaseResource(Resource):
    def __init__(self, api=None, *args, **kwargs):
        # self.context.logger = self.logger
        super(BaseResource, self).__init__(api, *args, **kwargs)

    def make_response(self, resp_code=None, resp_desc=None, data=None):
        if not resp_code:
            resp_code = SUCCESS
            resp_desc = u'成功'

        resp = dict(
            resp_code=resp_code,
            resp_desc=resp_desc
        )
        if data:
            resp['data'] = data
        return jsonify(resp)

    def _post(self, url, data, headers=None):
        data = json.dumps(data)
        resp = requests.post(url, data, headers=headers)
        return json.loads(resp.text)


class BaseResponse(Response):
    """
    response
    """
    def __init__(self, resp_code, resp_desc, timestamp=None, response=None, **kwargs):
        self.resp_code = resp_code
        self.resp_desc = resp_desc
        self.timestamp = timestamp if timestamp else str(time.time()).replace('.', '')



        if response is None:
            kwargs['response'] = json.dumps(self.get_base_response())
        super(BaseResponse, self).__init__(**kwargs)
        self.headers = self.get_response_headers()

    def get_response_headers(self):
        """
        获取响应头
        :return:
        """
        headers = {
            'content-type': 'application/json;charset=utf-8',
            'X-timestamp': self.timestamp
        }
        return headers

    def get_base_response(self):
        base_resp = dict(
            resp_code=self.resp_code,
            resp_desc=self.resp_desc,
        )

        return dict(resp=base_resp)





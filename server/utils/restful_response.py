#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from flask import jsonify

class ResultType(object):
    Success = 0
    Failed = 1


class CommonResponse(object):
    """
    xxx
    """

    def __init__(self, result=ResultType.Success, message=u'', data=None,resp_code = None,http_code=200):
        self.result = result
        self.message = message
        self.data = data
        self.http_code = http_code
        self.resp_code = resp_code
        super(CommonResponse, self).__init__()

    def to_json(self):
        return jsonify(result=self.result, message=self.message, data=self.data)


class ApiResponse(object):
    def __init__(self, resp_code = None,message=None, data=None,http_code=200):
        self.message = message
        self.data = data
        self.http_code = http_code
        self.resp_code = resp_code
        super(ApiResponse, self).__init__()

    def api_json(self):
        base_resp = {}
        resp = {}
        resp['resp_code'] = self.resp_code
        resp['resp_msg'] = self.message
        resp['timestamp'] =  int(round(time.time() * 1000))
        base_resp['resp'] = resp
        if self.data:
            base_resp.update(self.data)
        return base_resp,self.http_code


class PageQueryResponse(object):
    """
    分页查询响应信息
    """

    def __init__(self, total_num=0, row_list=[]):
        self.total_num = total_num
        self.row_list = row_list
        super(PageQueryResponse, self).__init__()

    def to_json(self):
        return jsonify(rows=self.row_list, total=self.total_num)


class ErrorResponse(object):
    """
    错误信息
    """

    def __init__(self, error_code=502, error_title='系统错误', error_content=None):
        self.error_code = error_code
        self.error_title = error_title
        self.error_content = error_content
        super(ErrorResponse, self).__init__()

    def to_json(self):
        return jsonify(error_code=self.error_code, error_title=self.error_title, error_content=self.error_content)

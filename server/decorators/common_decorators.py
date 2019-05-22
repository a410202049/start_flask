#!/usr/bin/env python
# coding: utf-8
import functools
from flask import request, url_for, session, redirect
import hashlib
from flask_restful import abort
from flask import current_app
import json

from server.controller.resource import BaseResource
from server.exception import ERROR, NOT_LOGIN

resource = BaseResource()


# def home_login_required(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         current_user = session.get('current_user', None)
#         if not current_user:
#             if request.is_xhr:
#                 return resource.make_response(ERROR, '请登录后，再继续操作')
#                 # return CommonResponse(ResultType.Failed, message=u"请登录后，再继续操作").to_json()
#             else:
#                 print 'not login'
#                 pass
#                 # return redirect(url_for('home.login'))
#         return func(*args, **kwargs)
#
#     return wrapper


def home_login_required(func):
    def wrapper(*args, **kwargs):
        current_user = session.get('current_user', None)
        if not current_user:
            if request.is_xhr:
                return resource.make_response(NOT_LOGIN, '请登录后，再继续操作')
                # return CommonResponse(ResultType.Failed, message=u"请登录后，再继续操作").to_json()
            else:
                print 'not login'
                pass
        return func(*args, **kwargs)
    return wrapper  # 返回
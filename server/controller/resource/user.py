#!/usr/bin/python
# -*- encoding: utf-8 -*-

from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_claims, get_jwt_identity, \
    create_refresh_token, jwt_refresh_token_required

from server.app import db
from server.controller.resource import v2, BaseResource

import hashlib

from server.exception import BusinessException, PASSWORD_NOT_MATCH
# from server.models.TestModel import User




# @v2.route('/login')
# class Login(BaseResource):
#     def post(self):
#         username = request.form.get('username')
#         password = request.form.get('password')
#
#         m1 = hashlib.md5()
#         m1.update(password.encode("utf-8"))
#         password_md5 = m1.hexdigest()
#
#         user_info = db.session.query(
#             User
#         ).filter(
#             User.username == username
#         ).first()
#
#         if user_info.password != password_md5:
#             raise BusinessException(u'密码不正确', PASSWORD_NOT_MATCH)
#
#         ret = {
#             'access_token': create_access_token(identity=username),
#             'refresh_token': create_refresh_token(identity=username)
#         }
#
#         return self.make_response(ret)
#
#
# @v2.route('/protected', methods=['GET'])
# class Protected(BaseResource):
#
#     @jwt_required
#     def get(self):
#         identity = get_jwt_identity()
#         claims = get_jwt_claims()
#         print claims
#         return identity
#
#
# @v2.route('/refresh', methods=['GET'])
# class Refresh(BaseResource):
#
#     @jwt_refresh_token_required
#     def get(self):
#         current_user = get_jwt_identity()
#         ret = {
#             'access_token': create_access_token(identity=current_user)
#         }
#         return self.make_response(ret)

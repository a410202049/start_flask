#!/usr/bin/python
# -*- encoding: utf-8 -*-
from flask_restplus import Resource, abort
from server.controller.resource import v2


# @v2.errorhandler(Exception)
# def api_handle_exception(error):
#     '''Return a custom message and 400 status code'''
#     print error
#     return {'message': 'What you want'}, 400

@v2.route('/users')
class Users(Resource):
    def get(self):
        return {"username": "kerry", "password":"123"}

    def post(self):
        return {"username": "kerry123", "password": "456"}

    def delete(self):
        return {"username": "kerry888", "password": "888"}


@v2.route('/users/<int:user_id>')
class UserDetail(Resource):
    def get(self, user_id):
        data = "123"
        a = 1 / 0
        # abort(400, 'My custom message', custom='value')
        # user = db.session.query(User).filter(
        #     User.id == user_id
        # ).first()
        # data = user.to_dict()
        # abort(404)
        return {"user_info": data}

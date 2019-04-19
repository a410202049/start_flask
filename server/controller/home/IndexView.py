#!/usr/bin/python
# -*- encoding: utf-8 -*-

from server.app import db
from server.controller.home import CommonView
from server.exception import BusinessException, PASSWORD_NOT_MATCH
from server.model.TestModel import Teacher, Student


class HomeBase(CommonView):

    def dispatch_request(self):
        context = {"school": {"name": u"北京大学"}}
        context.update(self.render_data())
        return self.render_template(context)


class HomeIndex(HomeBase):

    def render_data(self):
        return {}


class ArticleDetail(HomeBase):

    def render_data(self):
        return {}
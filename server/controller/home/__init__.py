#!/usr/bin/python
# -*- encoding: utf-8 -*-

from flask.views import View
from flask import Blueprint, render_template, current_app as app

from server.utils.log import FinalLogger

home = Blueprint('home', __name__)


class CommonView(View):
    def __init__(self, template_name):
        self.template_name = template_name
        # 初始化日志类
        logger = FinalLogger(app).get_logger()
        self.logger = logger

    def render_data(self,*args, **kwargs):
        return {}

    def get_template_name(self):
        raise NotImplementedError()

    def render_template(self, context):
        return render_template(self.template_name, **context)

    def dispatch_request(self, *args, **kwargs):
        context = dict()
        context.update(self.render_data(*args, **kwargs))
        return self.render_template(context)


from server.controller.home import IndexView
#!/usr/bin/python
# -*- encoding: utf-8 -*-

from flask.views import View
from flask import Blueprint, render_template, current_app as app

home = Blueprint('home', __name__)


class CommonView(View):
    def __init__(self, template_name):
        self.template_name = template_name
        self.logger = app.logger

    def render_data(self):
        return None

    def get_template_name(self):
        raise NotImplementedError()

    def render_template(self, context):
        return render_template(self.template_name, **context)

    def dispatch_request(self):
        context = dict()
        context.update(self.render_data())
        return self.render_template(context)


from server.controller.home import IndexView
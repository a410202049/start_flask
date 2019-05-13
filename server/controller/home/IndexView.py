#!/usr/bin/python
# -*- encoding: utf-8 -*-

from server.app import db
from server.controller.home import CommonView
from flask import session
from server.models.News import Customer

class HomeBase(CommonView):

    def dispatch_request(self, *args, **kwargs):
        current_user = session.get('current_user')
        context = {}
        if current_user:
            uid = current_user['uid']
            user_info = db.session.query(Customer).filter(
                Customer.id == uid
            ).first()
            context['user_info'] = user_info

        context.update(self.render_data(*args, **kwargs))
        return self.render_template(context)


class HomeIndex(HomeBase):
    pass


class ArticleDetail(HomeBase):

    def render_data(self, article_id):
        return {"username": "kerrygao", "article_id": article_id}
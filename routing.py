#!/usr/bin/python
# -*- encoding: utf-8 -*-
from server.controller.home.IndexView import HomeIndex, ArticleDetail

CONFIG = {
    'ENCODING': 'utf-8'
}

_app = None


def init_routing(app):
    print('init app in routing')

    app.add_url_rule('/', view_func=HomeIndex.as_view('index', template_name='index.html'), endpoint='index')
    app.add_url_rule('/article_detail/<article_id>',
                     view_func=ArticleDetail.as_view('article_detail',
                     template_name='article_detail.html'), endpoint='article_detail')


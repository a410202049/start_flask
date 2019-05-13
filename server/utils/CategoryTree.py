#!/usr/bin/python
# -*- encoding: utf-8 -*-
from flask import url_for


class CategoryTree(object):
    def __init__(self):
        self.parents = []

    def getPid(self,id,data):
        for da in data:
            if da.id == int(id):
                self.parents.insert(0,da)
                self.getPid(da.parent_id,data)
        return self.parents

    def render_category_html(self):
        html_string = ''
        for i,cate in enumerate(self.parents):
            j = i+1
            if j == len(self.parents):
                html_string+= '<a href="'+url_for('home.index',cid=cate.id)+'" >'+cate.name+ '</a>'
            else:
                html_string += '<a href="'+url_for('home.index',cid=cate.id)+'" >' + cate.name + '</a> / '
        return html_string
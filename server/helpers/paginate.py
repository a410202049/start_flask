#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import request, url_for,current_app as app
from flask_restful import Resource,marshal,fields,abort

class ApiPaginate(object):

    def __init__(self,data_obj = None,item_name = None,fields=None):
        self.data_obj = data_obj
        self.page_num = request.args.get('page_num', 1, type=int)
        self.page_size = request.args.get('page_size', app.config.get('API_PAGESIZE'),type=int)
        self.item_name = item_name
        self.fields = fields

    # @classmethod
    def api_page(self):
        paginate = self.data_obj.paginate(self.page_num, self.page_size)
        paginate_items = paginate.items
        items = {self.item_name:paginate_items}
        items_fields = marshal(items, self.fields)

        page = {
            'page_num': self.page_num,
            'page_size': self.page_size,
            'total': paginate.total,
            'pages': paginate.pages,
        }

        items_fields['page'] = page

        return items_fields

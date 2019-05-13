#!/usr/bin/python
# -*- encoding: utf-8 -*-
from server.models.Models import MenuAuth
import json
from flask import request
from server.app import db

class Auth(object):
    def __init__(self, user = None):
        self.user = user
        self.pids = []

    def auth_menus(self):
        path = request.path[1:]
        path = path +'index' if path == 'admin/' else path
        menus = db.session.query(
            MenuAuth
        ).order_by(MenuAuth.sort.asc()).filter(MenuAuth.type == 0).all()
        current_menus = db.session.query(MenuAuth).filter(MenuAuth.method == path).scalar()
        if current_menus:
            #获取所有父级菜单
            self.getPid(current_menus.id,menus)

        if str(self.user.group_id) == '1':
            return self.tree(menus)
        rules_str = self.user.group.rules
        rules = []
        if rules_str :
            rules = json.loads(rules_str)
        auth_menus = []
        for menu in menus:
            for rule_id in rules:
                if menu.id == rule_id:
                    auth_menus.append(menu)
        auth_menus = self.tree(auth_menus)
        return auth_menus

    def tree(self,data,pid = 0):
        tree_list = []
        for da in data:
            d = da.to_json()
            if d['is_show'] == 0:
                continue
            for p in self.pids:
                if d['id'] == p:
                    d['active'] = True
            if str(d.get('parent_id')) == str(pid):
                tmp = self.tree(data,d.get('id'))
                if tmp :
                    d['child'] = tmp
                tree_list.append(d)
        return tree_list

    def tree_list(self,data,pid = 0):
        tree_list = []
        for da in data:
            d = da.to_json()
            if str(d.get('parent_id')) == str(pid):
                tmp = self.tree_list(data,d.get('id'))
                tree_list.append(d)

                if tmp :
                    tree_list += tmp
        return tree_list

    def getPid(self,id,data):
        for da in data:
            if da.id == int(id):
                self.pids.append(da.id)
                self.getPid(da.parent_id,data)
        return self.pids


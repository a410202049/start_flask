# -*- coding:utf-8 -*-
from flask import Blueprint, request, json, current_app as app, render_template
import traceback

from server.app import db
from server.models.Models import MenuAuth
from server.utils.auth import Auth
from flask_login import current_user
from server.utils.restful_response import CommonResponse, ResultType


admin = Blueprint('admin', __name__, url_prefix='/admin')
from server.controller.admin.SiteBase import AuthView, BaseView, CommonView, ArticleView, FriendLinkView


@admin.before_request
def before_request():
    method = request.method
    header = request.headers.to_list()
    args = {
        'GET': request.args,
        'POST': request.form
    }[request.method]
    app.logger.info(
        '[request_url]{},[method]: {},[headers]:{},[args]:{}'.format(request.url, method, header, args.to_dict()))


# @admin.errorhandler(Exception)
# def code_exception_found(e):
#     trace = traceback.format_exc()
#     app.logger.info('\n[Exception] :\n {}\n'.format(trace))
#     return render_template('500.html'), 500

@admin.context_processor
def menus():
    user = current_user

    def check_auth(path):
        if user.is_active == True:
            if user.group_id == 1:
                return True
            all_menus = db.session.query(MenuAuth).order_by(MenuAuth.sort.asc()).all()
            rules_str = user.group.rules
            rules = []
            if rules_str:
                rules = json.loads(rules_str)
            all_menu_list = []
            auth_menu_list = []
            for menu in all_menus:
                all_menu_list.append(menu.method)
                for rule_id in rules:
                    if int(menu.id) == rule_id:
                        auth_menu_list.append(menu.method)

            if path in all_menu_list and path not in auth_menu_list:
                return False
            return True

    # 获取登陆后菜单
    if user.is_active == True:
        # 设置admin蓝图下全局变量
        auth = Auth(user)
        menus = auth.auth_menus()
        return {'menus': menus, 'check_auth': check_auth}
    return {'check_auth': check_auth}


# 权限验证
@admin.before_request
def before_request():
    user = current_user
    path = request.path[1:]
    path = path + 'index' if path == 'admin/' else path
    if user.is_active == True:
        if user.group_id == 1:
            return
        all_menus = db.session.query(MenuAuth).order_by(MenuAuth.sort.asc()).all()
        rules_str = user.group.rules
        rules = []
        if rules_str:
            rules = json.loads(rules_str)
        all_menu_list = []
        auth_menu_list = []
        for menu in all_menus:
            all_menu_list.append(menu.method)
            for rule_id in rules:
                if int(menu.id) == rule_id:
                    auth_menu_list.append(menu.method)

        if path in all_menu_list and path not in auth_menu_list:
            return CommonResponse(ResultType.Failed, message=u"没有权限").to_json()

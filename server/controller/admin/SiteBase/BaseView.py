#!/usr/bin/python
# -*- encoding: utf-8 -*-

from server.controller.admin import admin
from flask import render_template, request, current_app as app, json
from flask_login import login_required, current_user

from server.forms.forms import MenuForm, UserForm
from server.app import db
from server.models.CommonModel import SystemCfg, BannerCfg
from server.utils.restful_response import CommonResponse, ResultType
from server.models.Models import MenuAuth, User, UsersGroup
from server.utils.auth import Auth
from server.helpers.common_helper import tree, fragment


# 后台首页
@admin.route('/', methods=['GET', 'POST'])
@admin.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    title = u'系统首页'
    data = {}
    # 累加
    # db.session.query(PackageUser).filter(PackageUser.id == 5).update({"share_num": PackageUser.share_num + 1})
    # db.session.commit()
    return render_template('admin/index.html', data=data, title=title)


# 菜单查询
@admin.route('/menu-auth', methods=['GET', 'POST'])
@login_required
def menu_auth():
    title = u"菜单管理"
    menus = db.session.query(
        MenuAuth
    ).order_by(MenuAuth.sort.asc()).all()
    auth = Auth()
    menus = auth.tree_list(menus)
    return render_template('admin/menu_auth.html', data=menus, title=title)


# 获取菜单信息
@admin.route('/get-menu-info', methods=['GET', 'POST'])
@login_required
def get_menu_info():
    menu_id = request.form.get('menu_id')
    if not menu_id:
        return CommonResponse(ResultType.Failed, message=u"menu_id为空").to_json()
    menu_info_obj = db.session.query(MenuAuth).filter(MenuAuth.id == menu_id).scalar()
    if menu_info_obj is None:
        return CommonResponse(ResultType.Failed, message=u"菜单不存在").to_json()
    menu_info = menu_info_obj.to_json()
    return CommonResponse(ResultType.Success, message=u"获取成功", data=menu_info).to_json()


# 添加菜单
@admin.route('/menu-add', methods=['GET', 'POST'])
@login_required
def menu_add():
    form = MenuForm()
    try:
        if not form.validate():
            error_message = form.get_error()
            return CommonResponse(ResultType.Failed, message=error_message).to_json()
        else:
            menu = MenuAuth()
            menu.name = form.menu_name.data
            menu.method = form.method.data
            menu.type = form.type.data
            menu.icon = form.icon.data
            menu.sort = form.sort.data
            menu.is_show = form.is_show.data
            menu.parent_id = form.parent_id.data
            db.session.merge(menu)
            db.session.commit()
            return CommonResponse(ResultType.Success, message=u"添加成功").to_json()
    except Exception, e:
        db.session.rollback()
        return CommonResponse(ResultType.Failed, message=u"添加失败").to_json()


# 编辑菜单
@admin.route('/menu-edit', methods=['GET', 'POST'])
@login_required
def menu_edit():
    form = MenuForm()
    try:
        if not form.validate():
            error_message = form.get_error()
            return CommonResponse(ResultType.Failed, message=error_message).to_json()
        else:
            menu = MenuAuth()
            menu.id = form.id.data
            menu.name = form.menu_name.data
            menu.method = form.method.data
            menu.type = form.type.data
            menu.icon = form.icon.data
            menu.sort = form.sort.data
            menu.is_show = form.is_show.data
            menu.parent_id = form.parent_id.data
            db.session.merge(menu)
            db.session.commit()
            return CommonResponse(ResultType.Success, message=u"编辑成功").to_json()
    except Exception, e:
        db.session.rollback()
        return CommonResponse(ResultType.Failed, message=u"编辑失败").to_json()


# 删除菜单
@admin.route('/menu-del', methods=['GET', 'POST'])
@login_required
def menu_del():
    menu_id = request.form.get('menu_id')
    if not menu_id:
        return CommonResponse(ResultType.Failed, message=u"menu_id不能为空").to_json()
    menu_info_obj = db.session.query(MenuAuth).filter(MenuAuth.id == menu_id).scalar()
    if menu_info_obj is None:
        return CommonResponse(ResultType.Failed, message=u"菜单不存在").to_json()
    other_info_obj = db.session.query(MenuAuth).filter(MenuAuth.parent_id == menu_id).all()
    if other_info_obj:
        return CommonResponse(ResultType.Failed, message=u"删除菜单前，请先删除子菜单").to_json()

    db.session.delete(menu_info_obj)
    db.session.commit()
    return CommonResponse(ResultType.Success, message=u"删除成功").to_json()


# 用户管理
@admin.route('/user-manage', methods=['GET', 'POST'])
@login_required
def user_manage():
    title = u'用户管理'
    username = request.args.get('username', '')
    email = request.args.get('email', '')
    page = request.args.get('page', 1, type=int)
    user_obj = db.session.query(User).order_by(User.create_time.desc())
    if username != '':
        user_obj = user_obj.filter(User.username == username)
    if email != '':
        user_obj = user_obj.filter(User.email == email)

    paginate = user_obj.paginate(
        page, per_page=app.config['PAGE_SIZE'], error_out=True)
    users = paginate.items

    user_grops = db.session.query(UsersGroup).all()
    data = {
        "email": email,
        "username": username,
        "users": users,
        "pagination": paginate,
        "fragment": fragment(),
        "user_grops": user_grops
    }

    return render_template('admin/user_manage.html', data=data, title=title)


# 添加用户
@admin.route('/user-add', methods=['GET', 'POST'])
@login_required
def user_add():
    form = UserForm()
    try:
        if not form.validate():
            error_message = form.get_error()
            return CommonResponse(ResultType.Failed, message=error_message).to_json()
        else:
            user = User()
            user.username = form.username.data
            user.password = form.password.data
            user.email = form.email.data
            if form.group_id.data:
                user.group_id = form.group_id.data
            db.session.add(user)
            db.session.commit()
            return CommonResponse(ResultType.Success, message=u"添加成功").to_json()
    except Exception, e:
        db.session.rollback()
        return CommonResponse(ResultType.Failed, message=u"添加失败").to_json()


# 获取菜单信息
@admin.route('/get-user-info', methods=['GET', 'POST'])
@login_required
def get_user_info():
    user_id = request.form.get('user_id')
    if not user_id:
        return CommonResponse(ResultType.Failed, message=u"user_id不能为空").to_json()
    user_info_obj = db.session.query(User).filter(User.id == user_id).scalar()
    if user_info_obj is None:
        return CommonResponse(ResultType.Failed, message=u"用户不存在").to_json()
    user_info = user_info_obj.to_json()
    return CommonResponse(ResultType.Success, message=u"获取成功", data=user_info).to_json()


# 编辑用户
@admin.route('/user-edit', methods=['GET', 'POST'])
@login_required
def user_edit():
    form = UserForm()
    try:
        if not form.validate():
            error_message = form.get_error()
            return CommonResponse(ResultType.Failed, message=error_message).to_json()
        else:
            user = User()
            user.id = form.id.data
            user.username = form.username.data
            if form.password.data:
                user.password = form.password.data
            user.email = form.email.data
            if form.group_id.data:
                user.group_id = form.group_id.data
            else:
                user.group_id = None

            db.session.merge(user)
            db.session.commit()
            return CommonResponse(ResultType.Success, message=u"编辑成功").to_json()
    except Exception, e:
        db.session.rollback()
        return CommonResponse(ResultType.Failed, message=u"编辑失败").to_json()


# 删除用户
@admin.route('/user-del', methods=['GET', 'POST'])
@login_required
def user_del():
    user_id = request.form.get('user_id')
    if int(current_user.id) == int(user_id):
        return CommonResponse(ResultType.Failed, message=u"不能删除自己的账号").to_json()

    if user_id is None:
        return CommonResponse(ResultType.Failed, message=u"user_id不能为空").to_json()
    user_info_obj = db.session.query(User).filter(User.id == user_id).scalar()
    if user_info_obj is None:
        return CommonResponse(ResultType.Failed, message=u"用户不存在").to_json()

    db.session.delete(user_info_obj)
    db.session.commit()
    return CommonResponse(ResultType.Success, message=u"删除成功").to_json()


# 用户组管理
@admin.route('/user-group-manage', methods=['GET', 'POST'])
@login_required
def user_group_manage():
    title = u'用户组管理'
    name = request.args.get('name', '')
    status = request.args.get('status', '')

    page = request.args.get('page', 1, type=int)
    user_group_obj = db.session.query(UsersGroup).order_by(UsersGroup.create_time.desc())
    if name != '':
        user_group_obj = user_group_obj.filter(UsersGroup.name == name)
    if status != '' and status != 'ALL':
        user_group_obj = user_group_obj.filter(UsersGroup.status == status)

    paginate = user_group_obj.paginate(
        page, per_page=app.config['PAGE_SIZE'], error_out=True)
    groups = paginate.items

    data = {
        "name": name,
        "status": status,
        "pagination": paginate,
        "fragment": fragment(),
        "groups": groups
    }

    return render_template('admin/group_manage.html', data=data, title=title)


# 添加分组
@admin.route('/group-add', methods=['GET', 'POST'])
@login_required
def group_add():
    try:
        name = request.form.get('name')
        status = request.form.get('status', default=1)
        if not name:
            return CommonResponse(ResultType.Failed, message=u"分组名称不能为空").to_json()
        user_group_obj = db.session.query(UsersGroup).filter(UsersGroup.name == name).scalar()
        if user_group_obj:
            return CommonResponse(ResultType.Failed, message=u"分组名称不能重复").to_json()
        group = UsersGroup()
        group.name = name
        group.status = status
        db.session.merge(group)
        db.session.commit()

        return CommonResponse(ResultType.Success, message=u"添加成功").to_json()
    except Exception, e:
        db.session.rollback()
        return CommonResponse(ResultType.Failed, message=u"添加失败").to_json()


# 编辑分组
@admin.route('/group-edit', methods=['GET', 'POST'])
@login_required
def group_edit():
    try:
        id = request.form.get('id')
        name = request.form.get('name')
        status = request.form.get('status', default=1)
        if not name:
            return CommonResponse(ResultType.Failed, message=u"分组名称不能为空").to_json()
        user_group_obj = db.session.query(UsersGroup).filter(UsersGroup.id != id, UsersGroup.name == name).scalar()
        if user_group_obj:
            return CommonResponse(ResultType.Failed, message=u"分组名称不能重复").to_json()
        group = UsersGroup()
        group.id = id
        group.name = name
        group.status = status
        db.session.merge(group)
        db.session.commit()

        return CommonResponse(ResultType.Success, message=u"编辑成功").to_json()
    except Exception, e:
        db.session.rollback()
    return CommonResponse(ResultType.Failed, message=u"编辑失败").to_json()


# 获取分组权限
@admin.route('/get-rule-list', methods=['GET', 'POST'])
@login_required
def get_rule_list():
    group_id = request.form.get('group_id')
    menus = db.session.query(MenuAuth).all()
    groups_obj = db.session.query(UsersGroup).filter(UsersGroup.id == group_id).scalar()
    rules_str = groups_obj.rules
    user_rules = []
    if rules_str:
        user_rules = json.loads(rules_str)
    if user_rules:
        for index, menu in enumerate(menus):
            for rule in user_rules:
                if rule == menu.id:
                    menus[index].active = True
                    break
                menus[index].active = False
    else:
        for index, menu in enumerate(menus):
            menus[index].active = False
    data = []
    for menu in menus:
        da = {}
        da['id'] = menu.id
        da['active'] = menu.active
        da['name'] = menu.name
        da['parent_id'] = menu.parent_id
        data.append(da)
    ret = tree(data, pidName='parent_id')
    return CommonResponse(ResultType.Success, message=u"获取成功", data=ret).to_json()


# 获取分组信息
@admin.route('/get-group-info', methods=['GET', 'POST'])
@login_required
def get_group_info():
    group_id = request.form.get('group_id')
    if not group_id:
        return CommonResponse(ResultType.Failed, message=u"group_id不能为空").to_json()
    group_info_obj = db.session.query(UsersGroup).filter(UsersGroup.id == group_id).scalar()
    if group_info_obj is None:
        return CommonResponse(ResultType.Failed, message=u"分组不存在").to_json()
    group_info = group_info_obj.to_json()
    return CommonResponse(ResultType.Success, message=u"获取成功", data=group_info).to_json()


# 删除分组
@admin.route('/group-del', methods=['GET', 'POST'])
@login_required
def group_del():
    group_id = request.form.get('group_id')
    user_group_obj = db.session.query(UsersGroup).filter(UsersGroup.id == group_id).scalar()
    if user_group_obj is None:
        return CommonResponse(ResultType.Failed, message=u"分组不存在").to_json()
    user_obj = db.session.query(User).filter(User.group_id == group_id).all()
    if user_obj:
        return CommonResponse(ResultType.Failed, message=u"请先移除当前分组下的用户").to_json()

    db.session.delete(user_group_obj)
    db.session.commit()
    return CommonResponse(ResultType.Success, message=u"删除成功").to_json()


# 授权
@admin.route('/group_grant', methods=['GET', 'POST'])
@login_required
def group_grant():
    try:
        group_id = request.form.get('group_id')
        rules = request.form.get('rules')
        # rules = json.loads(rules_str)
        user_group_obj = db.session.query(UsersGroup).filter(UsersGroup.id == group_id).scalar()
        user_group_obj.rules = rules
        db.session.merge(user_group_obj)
        db.session.commit()
        return CommonResponse(ResultType.Success, message=u"授权成功").to_json()
    except Exception, e:
        db.session.rollback()
    return CommonResponse(ResultType.Failed, message=u"授权失败").to_json()


# 系统基本配置
@admin.route('/system_base_cfg', methods=['GET', 'POST'])
@login_required
def system_base_cfg():
    try:
        title = u"系统配置"
        sys_cfg = SystemCfg()
        data = {}
        data['site_name'] = sys_cfg.get_sys_value('site_name')
        data['site_keywords'] = sys_cfg.get_sys_value('site_keywords')
        data['site_description'] = sys_cfg.get_sys_value('site_description')
        data['third_code'] = sys_cfg.get_sys_value('third_code')

        data['email_smtp'] = sys_cfg.get_sys_value('email_smtp')
        data['email'] = sys_cfg.get_sys_value('email')
        data['email_password'] = sys_cfg.get_sys_value('email_password')

        banners = db.session.query(BannerCfg).order_by(BannerCfg.create_time.desc()).all()

        data['banners'] = banners

        return render_template('admin/system_base_cfg.html', data=data, title=title)
    except Exception, e:
        app.logger.info(e)
        return CommonResponse(ResultType.Failed, message=u"系统配置页面异常").to_json()


@admin.route('/save_base_cfg', methods=['GET', 'POST'])
@login_required
def save_base_cfg():
    try:
        site_name = request.form.get('site_name')
        site_keywords = request.form.get('site_keywords')
        site_description = request.form.get('site_description')
        third_code = request.form.get('third_code')
        sys_cfg = SystemCfg()
        sys_cfg.set_sys_value('site_name', site_name)
        sys_cfg.set_sys_value('site_keywords', site_keywords)
        sys_cfg.set_sys_value('site_description', site_description)
        sys_cfg.set_sys_value('third_code', third_code)
        return CommonResponse(ResultType.Success, message=u"保存成功").to_json()

    except Exception, e:
        app.logger.info(e)
        return CommonResponse(ResultType.Failed, message=u"保存系统基本配置异常").to_json()


@admin.route('/save_email_cfg', methods=['GET', 'POST'])
@login_required
def save_email_cfg():
    try:
        email_smtp = request.form.get('email_smtp')
        email = request.form.get('email')
        email_password = request.form.get('email_password')
        sys_cfg = SystemCfg()
        sys_cfg.set_sys_value('email_smtp', email_smtp)
        sys_cfg.set_sys_value('email', email)
        sys_cfg.set_sys_value('email_password', email_password)
        return CommonResponse(ResultType.Success, message=u"保存成功").to_json()
    except Exception, e:
        app.logger.info(e)
        return CommonResponse(ResultType.Failed, message=u"保存Email基本配置异常").to_json()

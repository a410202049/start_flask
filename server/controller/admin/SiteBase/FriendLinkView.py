#!/usr/bin/python
# -*- encoding: utf-8 -*-

from server.controller.admin import admin
from flask_login import current_user, login_required
from flask import render_template, request, current_app as app, json
from server.helpers.common_helper import fragment, is_number
from server.app import db
from server.utils.restful_response import CommonResponse, ResultType
from server.models.FriendLinkModel import FriendLink


@admin.route('/friend-link', methods=['GET', 'POST'])
@login_required
def friend_link():
    try:
        title = u'链接管理'

        page = request.args.get('page', 1, type=int)
        link_name = request.args.get('link_name', '')
        rows = db.session.query(
            FriendLink
        ).order_by(FriendLink.create_time.desc())

        if link_name:
            rows = rows.filter(
                FriendLink.name.like("%{0}%".format(link_name))
            )

        paginate = rows.paginate(page, per_page=app.config['PAGE_SIZE'], error_out=True)
        items = paginate.items

        data = {
            "link_name": link_name,
            "links": items,
            "pagination": paginate,
            "fragment": fragment()
        }
        return render_template('admin/friend_link.html', title=title, data=data)
    except Exception, e:
        app.logger.info(e)


@admin.route('/add_link_method', methods=['POST'])
@login_required
def add_link_method():
    try:
        form = request.form

        link_name = form.get('link_name')
        link_icon = form.get('cover_pic')
        sort = form.get('sort')
        link_href = form.get('link_href')
        link_type = form.get('link_type')
        friend_link = FriendLink()

        if not link_name:
            return CommonResponse(ResultType.Failed, message=u"链接名称不能为空").to_json()
        if link_type == 'pic_link' and not link_icon:
            return CommonResponse(ResultType.Failed, message=u"链接图片不能为空").to_json()

        friend_link.name = link_name
        friend_link.link_icon = link_icon
        friend_link.link_type = link_type
        friend_link.link_href = link_href
        friend_link.sort = sort
        db.session.add(friend_link)
        db.session.commit()

        return CommonResponse(ResultType.Success, message=u"添加成功").to_json()
    except Exception, e:
        app.logger.info(e)
        return CommonResponse(ResultType.Failed, message=u"添加链接出现异常").to_json()


@admin.route('/edit_link_method', methods=['POST'])
@login_required
def edit_link_method():
    try:
        form = request.form
        id = form.get('id')
        link_name = form.get('link_name')
        link_icon = form.get('cover_pic')
        sort = form.get('sort')
        link_href = form.get('link_href')
        link_type = form.get('link_type')

        if not link_name:
            return CommonResponse(ResultType.Failed, message=u"链接名称不能为空").to_json()
        if link_type == 'pic_link' and not link_icon:
            return CommonResponse(ResultType.Failed, message=u"链接图片不能为空").to_json()

        friend_link = db.session.query(FriendLink).filter(
            FriendLink.id == id
        ).first()

        friend_link.name = link_name
        friend_link.link_icon = link_icon
        friend_link.link_type = link_type
        friend_link.link_href = link_href
        friend_link.sort = sort
        db.session.merge(friend_link)
        db.session.commit()

        return CommonResponse(ResultType.Success, message=u"编辑成功").to_json()
    except Exception, e:
        app.logger.info(e)
    return CommonResponse(ResultType.Failed, message=u"编辑链接出现异常").to_json()


# 删除分类
@admin.route('/del_link_method', methods=['GET', 'POST'])
@login_required
def del_link_method():
    try:
        link_id = request.form.get('link_id')
        if not link_id:
            return CommonResponse(ResultType.Failed, message=u"link_id不能为空").to_json()
        link_info_obj = db.session.query(FriendLink).filter(FriendLink.id == link_id).scalar()
        if link_info_obj is None:
            return CommonResponse(ResultType.Failed, message=u"链接不存在").to_json()

        db.session.delete(link_info_obj)
        db.session.commit()
        return CommonResponse(ResultType.Success, message=u"删除成功").to_json()
    except Exception, e:
        app.logger.info(e)
        return CommonResponse(ResultType.Failed, message=u"删除失败").to_json()


@admin.route('/get_link_info', methods=['POST'])
@login_required
def get_link_info():
    try:
        form = request.form
        link_id = form.get('link_id')

        if not link_id:
            return CommonResponse(ResultType.Failed, message=u"link_id不能为空").to_json()
        link_obj = db.session.query(FriendLink).filter(FriendLink.id == link_id).scalar()
        if link_obj is None:
            return CommonResponse(ResultType.Failed, message=u"链接不存在").to_json()
        link_info = link_obj.to_json()
        return CommonResponse(ResultType.Success, message=u"获取成功", data=link_info).to_json()
    except Exception, e:
        app.logger.info(e)
        return CommonResponse(ResultType.Failed, message=u"获取分类出现异常").to_json()

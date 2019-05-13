#!/usr/bin/python
# -*- encoding: utf-8 -*-

from server.controller.admin import admin
from flask import request, current_app as app, url_for
from flask_login import login_required
from server.app import db
from server.models.CommonModel import BannerCfg
from server.utils.Upload import Upload

from server.utils.restful_response import CommonResponse, ResultType
from server.models.ArticleModel import ArticleKeywords
from sqlalchemy import or_


@admin.route('/upload', methods=['POST'])
def upload():
    upload = Upload()
    pic_path = upload.upload_file()
    return CommonResponse(ResultType.Success, message=u"获取成功", data={"img_path": url_for('static',
                                                                                         filename=pic_path,
                                                                                         _external=True)}).to_json()


@admin.route('/get_keyword_list', methods=['GET', 'POST'])
@login_required
def get_keyword_list():
    try:
        keyword = request.form.get('keyword', '')
        pageNumber = request.form.get('pageNumber', 1, type=int)
        pageSize = request.form.get('pageSize', app.config['PAGE_SIZE'], type=int)
        searchKey = request.form.get('searchKey', None)
        searchValue = request.form.get('searchValue', None)

        rows = db.session.query(ArticleKeywords)

        if searchKey and searchValue:
            ids = searchValue.split(',')
            rows = rows.filter(
                ArticleKeywords.id.in_(ids)
            )
        if keyword:
            rows = rows.filter(or_(
                ArticleKeywords.name.like(u'%{0}%'.format(keyword)),
            ))

        paginate = rows.paginate(
            pageNumber, per_page=pageSize, error_out=True)

        provice_list = paginate.items

        data_list = []

        for item in provice_list:
            data_list.append(item.to_json())
        data = {
            "pageSize": pageSize,
            "pageNumber": pageNumber,
            "totalRow": paginate.total,
            "totalPage": paginate.pages,
            "list": data_list
        }

        return CommonResponse(ResultType.Success, message=u"获取成功", data=data).to_json()
    except Exception, e:
        app.logger.info(e)
        return CommonResponse(ResultType.Failed, message=u"获取关键词列表出现错误").to_json()


@admin.route('/get_keyword_info', methods=['GET', 'POST'])
@login_required
def get_keyword_info():
    try:
        keyword_id = request.form.get('keyword_id')
        keyword = db.session.query(
            ArticleKeywords
        ).filter(
            ArticleKeywords.id == keyword_id
        ).first()
        data = keyword.to_json()
        return CommonResponse(ResultType.Success, message=u"获取成功", data=data).to_json()
    except Exception, e:
        app.logger.info(e)
    return CommonResponse(ResultType.Failed, message=u"获取关键词出现错误").to_json()


@admin.route('/add_banner', methods=['GET', 'POST'])
@login_required
def add_banner():
    try:
        title = request.form.get('title')
        description = request.form.get('description')
        img_url = request.form.get('img_url')
        sort = request.form.get('sort')
        href = request.form.get('href')

        banner = BannerCfg()
        banner.title = title
        banner.href = href
        banner.description = description
        banner.img_url = img_url
        banner.sort = sort
        db.session.add(banner)
        db.session.commit()

        return CommonResponse(ResultType.Success, message=u"添加成功", ).to_json()
    except Exception, e:
        app.logger.info(e)
    return CommonResponse(ResultType.Failed, message=u"编辑出现错误").to_json()


@admin.route('/edit_banner', methods=['GET', 'POST'])
@login_required
def edit_banner():
    try:
        banner_id = request.form.get('banner_id')
        title = request.form.get('title')
        description = request.form.get('description')
        href = request.form.get('href')
        img_url = request.form.get('img_url')
        sort = request.form.get('sort')
        banner = db.session.query(BannerCfg).filter(
            BannerCfg.id == banner_id
        ).first()
        banner.title = title
        banner.description = description
        banner.href = href
        banner.img_url = img_url
        banner.sort = sort
        db.session.merge(banner)
        db.session.commit()
        return CommonResponse(ResultType.Success, message=u"编辑成功").to_json()
    except Exception, e:
        app.logger.info(e)
    return CommonResponse(ResultType.Failed, message=u"编辑出现错误").to_json()


@admin.route('/del_banner', methods=['GET', 'POST'])
@login_required
def del_banner():
    try:
        banner_id = request.form.get('banner_id')

        db.session.query(BannerCfg).filter(
            BannerCfg.id == banner_id
        ).delete()
        db.session.commit()
        return CommonResponse(ResultType.Success, message=u"删除成功", ).to_json()
    except Exception, e:
        app.logger.info(e)
    return CommonResponse(ResultType.Failed, message=u"删除Banner出现错误").to_json()


@admin.route('/get_banner_info', methods=['GET', 'POST'])
@login_required
def get_banner_info():
    try:
        banner_id = request.form.get('banner_id')

        data = db.session.query(BannerCfg).filter(
            BannerCfg.id == banner_id
        ).first()
        return CommonResponse(ResultType.Success, message=u"获取成功", data=data.to_json()).to_json()
    except Exception, e:
        app.logger.info(e)
    return CommonResponse(ResultType.Failed, message=u"获取成功Banner出现错误").to_json()

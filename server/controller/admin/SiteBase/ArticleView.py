#!/usr/bin/python
# -*- encoding: utf-8 -*-

from server.controller.admin import admin
# from app.controller.admin import admin
from flask import render_template, request, current_app as app, json
from server.app import db
from server.helpers.common_helper import fragment
from server.models.ArticleModel import ArticleCategory, Article, ArticleKeywordRelation, ArticleKeywords
from server.models.Models import User
from server.utils.XssFilter import XssHtml
from server.utils.auth import Auth
from server.utils.restful_response import CommonResponse, ResultType
from flask_login import current_user, login_required


@admin.route('/article_list', methods=['GET', 'POST'])
@login_required
def article_list():
    try:
        title = u'文章列表'

        article_title = request.args.get('title', '')
        category_id = request.args.get('category_id', '')
        page = request.args.get('page', 1, type=int)

        categorys_data = ArticleCategory.get_category_all()
        categorys = []
        for category in categorys_data:
            cate = {}
            cate['id'] = category.id
            cate['name'] = category.name
            cate['cover_pic'] = category.cover_pic
            cate['description'] = category.description
            cate['sort'] = category.sort
            cate['pid'] = category.parent_id
            categorys.append(cate)
        categorys_json = json.dumps(categorys)

        category_obj = ArticleCategory.get_category(category_id)

        rows = db.session.query(
            Article.id,
            ArticleCategory.name.label('category_name'),
            Article.title,
            Article.is_top,
            Article.is_hot,
            Article.view_num,
            Article.create_time,
            User.username,
            User.nickname
        ).outerjoin(
            User, Article.author_id == User.id
        ).join(
            ArticleCategory, Article.cid == ArticleCategory.id
        ).order_by(Article.create_time.desc())
        if article_title:
            rows = rows.filter(
                Article.title.like(u'%{0}%'.format(article_title)),
            )

        if category_id:
            rows = rows.filter(
                Article.cid == category_id
            )

        paginate = rows.paginate(
            page, per_page=app.config['PAGE_SIZE'], error_out=True)

        articles = paginate.items

        data = {
            "title": article_title,
            "category_id": category_id,
            "category_name": category_obj.name if category_obj else '',
            "articles": articles,
            "pagination": paginate,
            "fragment": fragment()
        }

        return render_template('admin/article_list.html', data=data, title=title, categorys_json=categorys_json)
    except Exception, e:
        app.logger.info(e)


@admin.route('/article_add', methods=['GET', 'POST'])
@login_required
def article_add():
    try:
        title = u'添加文章'

        article_category = ArticleCategory()
        categorys_data = article_category.get_category_all()
        categorys = []

        for category in categorys_data:
            cate = {}
            cate['id'] = category.id
            cate['name'] = category.name
            cate['cover_pic'] = category.cover_pic
            cate['description'] = category.description
            cate['sort'] = category.sort
            cate['pid'] = category.parent_id
            categorys.append(cate)
        categorys_json = json.dumps(categorys)

        return render_template('admin/article_add.html', data=categorys_data, title=title,
                               categorys_json=categorys_json)
    except Exception, e:
        app.logger.info(e)


@admin.route('/article_add_method', methods=['POST'])
@login_required
def article_add_method():
    try:
        form = request.form
        title = form.get('title')
        category_id = form.get('category_id')
        cover_pic = form.get('cover_pic')
        description = form.get('description')
        content = form.get('content')
        keywords = form.get('keywords')
        is_top = form.get('is_top')
        is_hot = form.get('is_hot')
        source = form.get('source')
        source_site = form.get('source_site')

        if not title:
            return CommonResponse(ResultType.Failed, message=u"标题不能为空").to_json()
        if not category_id:
            return CommonResponse(ResultType.Failed, message=u"请选择分类").to_json()
        if not content:
            return CommonResponse(ResultType.Failed, message=u"请填写文章内容").to_json()

        article = Article()
        article.title = title

        parser = XssHtml()
        parser.feed(content)
        parser.close()
        content_html = parser.getHtml()
        article.content = content_html
        article.is_top = is_top
        article.is_hot = is_hot
        article.cover_pic = cover_pic
        article.description = description
        article.author_id = current_user.id
        article.cid = category_id
        article.source = source
        article.source_site = source_site

        db.session.add(article)
        db.session.commit()
        article_id = article.id
        if keywords:
            keyword_list = keywords.split(',')
            for keyword_id in keyword_list:
                article_relation = ArticleKeywordRelation()
                article_relation.article_id = article_id
                article_relation.keyword_id = keyword_id
                db.session.add(article_relation)
            db.session.commit()
        return CommonResponse(ResultType.Success, message=u"添加成功").to_json()
    except Exception, e:
        app.logger.info(e)
        return CommonResponse(ResultType.Failed, message=u"添加文章出现异常").to_json()


@admin.route('/article_edit', methods=['GET', 'POST'])
@login_required
def article_edit():
    try:
        title = u'编辑文章'

        article_category = ArticleCategory()
        categorys_data = article_category.get_category_all()
        categorys = []

        article_id = request.args.get('article_id')
        article = Article.get_article(article_id)

        keyword_ids = ArticleKeywordRelation.get_keyword_ids(article_id)
        keywords = ",".join(keyword_ids)
        category_data = ArticleCategory.get_category(article.cid)
        for category in categorys_data:
            cate = {}
            cate['id'] = category.id
            cate['name'] = category.name
            cate['cover_pic'] = category.cover_pic
            cate['description'] = category.description
            cate['sort'] = category.sort
            cate['pid'] = category.parent_id
            categorys.append(cate)
        categorys_json = json.dumps(categorys)

        return render_template('admin/article_edit.html', data=categorys_data, title=title,
                               categorys_json=categorys_json, keywords=keywords, article=article,
                               category_data=category_data)
    except Exception, e:
        app.logger.info(e)


@admin.route('/article_edit_method', methods=['POST'])
@login_required
def article_edit_method():
    try:
        form = request.form
        title = form.get('title')
        category_id = form.get('category_id')
        cover_pic = form.get('cover_pic')
        description = form.get('description')
        content = form.get('content')
        keywords = form.get('keywords')
        is_top = form.get('is_top')
        is_hot = form.get('is_hot')
        article_id = form.get('article_id')
        source = form.get('source')
        source_site = form.get('source_site')

        if not title:
            return CommonResponse(ResultType.Failed, message=u"标题不能为空").to_json()
        if not category_id:
            return CommonResponse(ResultType.Failed, message=u"请选择分类").to_json()
        if not content:
            return CommonResponse(ResultType.Failed, message=u"请填写文章内容").to_json()

        article = db.session.query(Article).filter(
            Article.id == article_id
        ).first()
        article.title = title

        parser = XssHtml()
        parser.feed(content)
        parser.close()
        content_html = parser.getHtml()

        article.content = content_html
        article.is_top = is_top
        article.is_hot = is_hot
        article.cover_pic = cover_pic
        article.description = description
        article.author_id = current_user.id
        article.cid = category_id
        article.source = source
        article.source_site = source_site
        db.session.merge(article)
        db.session.commit()
        if keywords:
            ArticleKeywordRelation.del_keyword(article_id)
            keyword_list = keywords.split(',')
            for keyword_id in keyword_list:
                article_relation = ArticleKeywordRelation()
                article_relation.article_id = article_id
                article_relation.keyword_id = keyword_id
                db.session.add(article_relation)
            db.session.commit()
        return CommonResponse(ResultType.Success, message=u"编辑成功").to_json()
    except Exception, e:
        app.logger.info(e)
        return CommonResponse(ResultType.Failed, message=u"编辑文章出现异常").to_json()


@admin.route('/article_del_method', methods=['POST'])
@login_required
def article_del_method():
    try:
        form = request.form
        article_id = form.get('article_id')
        db.session.query(Article).filter(
            Article.id == article_id
        ).delete()
        db.session.commit()
        return CommonResponse(ResultType.Success, message=u"删除成功").to_json()
    except Exception, e:
        app.logger.info(e)
        return CommonResponse(ResultType.Failed, message=u"删除文章出现异常").to_json()


@admin.route('/article_category_list', methods=['GET'])
@login_required
def article_category_list():
    try:
        title = u'文章分类'
        categorys_data = ArticleCategory.get_category_all()
        auth = Auth()
        categorys = auth.tree_list(categorys_data)

        data = {
            "categorys_list": categorys,
        }
        return render_template('admin/article_category_list.html', data=data, title=title)
    except Exception as e:
        app.logger.info(e)


@admin.route('/add_category_method', methods=['POST'])
@login_required
def add_category_method():
    try:
        form = request.form
        category_name = form.get('category_name')
        description = form.get('description')
        sort = form.get('sort')
        pid = form.get('pid')

        if not category_name:
            return CommonResponse(ResultType.Failed, message=u"分类名称不能为空").to_json()

        category = ArticleCategory()
        category.name = category_name
        category.description = description
        category.sort = sort
        category.parent_id = pid if pid else 0
        db.session.add(category)
        db.session.commit()

        return CommonResponse(ResultType.Success, message=u"添加成功").to_json()
    except Exception, e:
        app.logger.info(e)
        return CommonResponse(ResultType.Failed, message=u"添加分类出现异常").to_json()


@admin.route('/get_category_info', methods=['POST'])
@login_required
def get_category_info():
    try:
        form = request.form
        category_id = form.get('category_id')

        if not category_id:
            return CommonResponse(ResultType.Failed, message=u"category_id为空").to_json()
        category_info_obj = db.session.query(ArticleCategory).filter(ArticleCategory.id == category_id).scalar()
        if category_info_obj is None:
            return CommonResponse(ResultType.Failed, message=u"分类不存在").to_json()
        category_info = category_info_obj.to_json()
        return CommonResponse(ResultType.Success, message=u"获取成功", data=category_info).to_json()
    except Exception, e:
        app.logger.info(e)
        return CommonResponse(ResultType.Failed, message=u"添加分类出现异常").to_json()


# 编辑菜单
@admin.route('/edit_category_method', methods=['GET', 'POST'])
@login_required
def edit_category_method():
    form = request.form
    category_name = form.get('category_name')
    description = form.get('description')
    sort = form.get('sort')
    pid = form.get('pid')
    id = form.get('id')

    if not category_name:
        return CommonResponse(ResultType.Failed, message=u"分类名称不能为空").to_json()
    try:

        category = ArticleCategory()
        category.id = id
        category.name = category_name
        category.description = description
        category.sort = sort
        category.parent_id = pid

        db.session.merge(category)
        db.session.commit()
        return CommonResponse(ResultType.Success, message=u"编辑成功").to_json()
    except Exception, e:
        app.logger.info(e)
        return CommonResponse(ResultType.Failed, message=u"编辑失败").to_json()


# 删除分类
@admin.route('/del_category_method', methods=['GET', 'POST'])
@login_required
def del_category_method():
    try:
        category_id = request.form.get('category_id')
        if not category_id:
            return CommonResponse(ResultType.Failed, message=u"category_id不能为空").to_json()
        category_info_obj = db.session.query(ArticleCategory).filter(ArticleCategory.id == category_id).scalar()

        if category_info_obj is None:
            return CommonResponse(ResultType.Failed, message=u"分类不存在").to_json()
        other_info_obj = db.session.query(ArticleCategory).filter(ArticleCategory.parent_id == category_id).all()

        articles = db.session.query(
            Article
        ).filter(
            Article.cid == category_id
        ).all()
        if articles:
            return CommonResponse(ResultType.Failed, message=u"请先删除，当前分类下的文章").to_json()
        if other_info_obj:
            return CommonResponse(ResultType.Failed, message=u"删除分类前，请先删除子分类").to_json()
        db.session.delete(category_info_obj)
        db.session.commit()
        return CommonResponse(ResultType.Success, message=u"删除成功").to_json()
    except Exception, e:
        app.logger.info(e)
        return CommonResponse(ResultType.Failed, message=u"删除失败").to_json()


@admin.route('/article_keywords_list', methods=['GET'])
@login_required
def article_keywords_list():
    try:
        title = u'关键词列表'
        page = request.args.get('page', 1, type=int)
        rows = db.session.query(ArticleKeywords)
        paginate = rows.paginate(
            page, per_page=app.config['PAGE_SIZE'], error_out=True)

        keywords = paginate.items

        data = {
            "keywords": keywords,
            "pagination": paginate,
            "fragment": fragment()
        }
        return render_template('admin/article_keywords_list.html', data=data, title=title)
    except Exception as e:
        app.logger.info(e)


@admin.route('/add_article_keywords_method', methods=['POST'])
@login_required
def add_article_keywords_method():
    try:
        keyword = request.form.get('keyword')
        if not keyword:
            return CommonResponse(ResultType.Failed, message=u"关键词不能为空").to_json()
        keyword_data = db.session.query(ArticleKeywords).filter(ArticleKeywords.name == keyword).first()
        if keyword_data:
            return CommonResponse(ResultType.Failed, message=u"关键词已存在").to_json()

        article_keyword = ArticleKeywords()
        article_keyword.name = keyword
        db.session.add(article_keyword)
        db.session.commit()
        return CommonResponse(ResultType.Success, message=u"添加成功").to_json()
    except Exception, e:
        app.logger.info(e)
        return CommonResponse(ResultType.Failed, message=u"添加失败").to_json()


@admin.route('/edit_article_keywords_method', methods=['POST'])
@login_required
def edit_article_keywords_method():
    try:
        keyword = request.form.get('keyword')
        keyword_id = request.form.get('keyword_id')
        if not keyword:
            return CommonResponse(ResultType.Failed, message=u"关键词不能为空").to_json()

        keyword_data = db.session.query(ArticleKeywords).filter(ArticleKeywords.name == keyword,
                                                                ArticleKeywords.id != keyword_id).first()
        if keyword_data:
            return CommonResponse(ResultType.Failed, message=u"关键词已存在").to_json()

        article_keyword = db.session.query(ArticleKeywords).filter(ArticleKeywords.id == keyword_id).first()
        article_keyword.name = keyword
        db.session.merge(article_keyword)
        db.session.commit()
        return CommonResponse(ResultType.Success, message=u"编辑成功").to_json()
    except Exception, e:
        app.logger.info(e)
        return CommonResponse(ResultType.Failed, message=u"编辑失败").to_json()


@admin.route('/del_article_keywords_method', methods=['POST'])
@login_required
def del_article_keywords_method():
    try:
        keyword_id = request.form.get('keyword_id')
        if not keyword_id:
            return CommonResponse(ResultType.Failed, message=u"关键词id不能为空").to_json()
        db.session.query(ArticleKeywords).filter(ArticleKeywords.id == keyword_id).delete()
        db.session.query(
            ArticleKeywordRelation
        ).filter(ArticleKeywordRelation.keyword_id == keyword_id).delete()
        db.session.commit()
        return CommonResponse(ResultType.Success, message=u"删除成功").to_json()
    except Exception, e:
        app.logger.info(e)
        return CommonResponse(ResultType.Failed, message=u"删除失败").to_json()

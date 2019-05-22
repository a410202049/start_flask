#!/usr/bin/python
# -*- encoding: utf-8 -*-
import random
from datetime import datetime, timedelta
import re

from flask import request, session, current_app, redirect, url_for
from server.app import db
from server.controller.resource import v2, BaseResource

import hashlib

from server.decorators.common_decorators import home_login_required
from server.exception import BusinessException, PASSWORD_NOT_MATCH, ERROR, SUCCESS, ADD_COLLET_SUCCESS, \
    CANCEL_COLLET_SUCCESS
from server.helpers.common_helper import friendly_time
from server.models.ArticleModel import Article, ArticleCategory
from server.models.News import Customer, MobileCodeRecord, ArticleCollet


@v2.route('/register')
class Register(BaseResource):
    def post(self):
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        verifi_code = request.form.get('verifi_code')
        regx = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
        phonematch = regx.match(mobile)

        if not verifi_code:
            return self.make_response(ERROR, u'请输入验证码')

        if not phonematch:
            return self.make_response(ERROR, u'手机格式不正确')

        user = db.session.query(Customer).filter(
            Customer.username == mobile
        ).first()
        if user:
            return self.make_response(ERROR, u"该手机号已经被注册")

        verifi_code_obj = db.session.query(MobileCodeRecord).filter(
            MobileCodeRecord.mobile == mobile,
            MobileCodeRecord.is_use == 0
        ).order_by(MobileCodeRecord.create_time.desc()).first()

        if not verifi_code_obj:
            return self.make_response(ERROR, u"请先获取验证码")

        if verifi_code_obj and verifi_code_obj.code != verifi_code:
            return self.make_response(ERROR, u"验证码错误")

        m1 = hashlib.md5()
        m1.update(password.encode("utf-8"))
        password_md5 = m1.hexdigest()

        customer = Customer()
        customer.username = mobile
        customer.mobile = mobile
        customer.nickname = mobile
        customer.is_mobile_auth = 1
        customer.password = password_md5

        db.session.add(customer)
        verifi_code_obj.is_use = 1
        db.session.merge(verifi_code_obj)
        db.session.commit()
        return self.make_response(SUCCESS, u"注册成功")


@v2.route('/login')
class Login(BaseResource):
    def post(self):
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        regx = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
        phonematch = regx.match(mobile)

        m1 = hashlib.md5()
        m1.update(password.encode("utf-8"))
        password_md5 = m1.hexdigest()

        if not phonematch:
            return self.make_response(ERROR, u'手机格式不正确')

        user = db.session.query(Customer).filter(
            Customer.username == mobile
        ).first()
        if not user:
            return self.make_response(ERROR, u'用户不存在')
        if user.password != password_md5:
            return self.make_response(ERROR, u'密码不正确')

        session['current_user'] = {
            "uid": user.id
        }
        return self.make_response(SUCCESS, u"登录成功")


@v2.route('/logout')
class Logout(BaseResource):
    def get(self):
        session.pop('current_user', None)
        return redirect(url_for('index'))


@v2.route('/send-msg-code')
class SendMsgCode(BaseResource):
    def post(self):

        mobile = request.form.get('mobile')
        ip = request.remote_addr

        regx = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
        phonematch = regx.match(mobile)
        if not phonematch:
            return self.make_response(ERROR, u'手机格式不正确')

        one_hour = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")

        count = db.session.query(MobileCodeRecord).filter(
            MobileCodeRecord.mobile == mobile,
            MobileCodeRecord.create_time >= one_hour,
            MobileCodeRecord.ip == ip
        ).count()

        #一小时之内最多发五次
        if count >= 5:
            return self.make_response(ERROR, u'验证码不能获取太频繁')
        secucode = '%04d' % random.randint(0, 9999)

        para = {
            "sid": current_app.config.get('SID'),
            "token": current_app.config.get('TOKEN'),
            "appid": current_app.config.get('APPID'),
            "templateid": current_app.config.get('TEMPLATE_ID'),
            "mobile": mobile,
            "param": secucode
        }

        headers = {"Content-Type": "application/json"}

        # resp = self._post(current_app.config.get('MSG_URL'), para, headers)
        #
        # if resp['code'] != '000000':
        #     return self.make_response(ERROR, u'短信发送失败')

        mobile_record = MobileCodeRecord()
        mobile_record.mobile = mobile
        mobile_record.ip = ip
        mobile_record.code = secucode
        db.session.add(mobile_record)
        db.session.commit()
        return self.make_response(SUCCESS, u'发送成功')


@v2.route('/more-article/<int:page>', endpoint="more-article")
class MoreArticle(BaseResource):
    def get(self, page):
        page_size = request.args.get('page_size', 2)
        # page = request.args.get('page', 2)

        top_article_obj = db.session.query(
            Article.id,
            Article.title,
            Article.description,
            Article.cover_pic,
            Article.create_time,
            ArticleCategory.name.label('category_name')
        ).join(
            ArticleCategory, ArticleCategory.id == Article.cid
        ).filter(
            Article.is_top == 1
        ).order_by(Article.create_time.desc()).paginate(int(page), int(page_size), False)

        top_article_items = top_article_obj.items

        top_articles = []
        for top_article in top_article_items:
            _ = {}
            _['id'] = top_article.id
            _['title'] = top_article.title
            _['description'] = top_article.description
            _['cover_pic'] = top_article.cover_pic
            _['create_time'] = friendly_time(top_article.create_time)
            _['category_name'] = top_article.category_name
            _['article_url'] = url_for('article_detail', article_id=top_article.id, _external=True)

            top_articles.append(_)

        if not top_articles:
            return self.make_response(ERROR, u'没有更多资讯了')

        return self.make_response(SUCCESS, u'加载成功', data=top_articles)


@v2.route('/article-collet/<int:article_id>', endpoint="article-collet")
class ArticleColletResource(BaseResource):
    @home_login_required
    def get(self, article_id):
        current_user = session.get('current_user', None)
        uid = current_user['uid']

        article = db.session.query(
            Article
        ).filter(
            Article.id == article_id
        ).first()

        if article.author_id == uid:
            return self.make_response(ERROR, u'不能收藏自己发布的文章')

        collet = db.session.query(
            ArticleCollet
        ).filter(
            ArticleCollet.article_id == article_id,
            ArticleCollet.uid == uid
        ).first()
        if not collet:
            article_collet = ArticleCollet()
            article_collet.uid = uid
            article_collet.article_id = article_id
            db.session.add(article_collet)
            db.session.commit()
            return self.make_response(ADD_COLLET_SUCCESS, u'添加收藏')
        else:
            db.session.delete(collet)
            db.session.commit()
            return self.make_response(CANCEL_COLLET_SUCCESS, u'取消收藏')
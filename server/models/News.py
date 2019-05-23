#!/usr/bin/python
# -*- encoding: utf-8 -*-
from server.app import db
from datetime import datetime
from sqlalchemy import DATETIME, String
from sqlalchemy import Column


class Customer(db.Model):
    __tablename__ = 't_customer'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), doc=u'用户名', nullable=False)
    password = db.Column(db.String(32), doc=u'密码', nullable=False)
    nickname = db.Column(db.String(50), doc=u'昵称', nullable=True)
    mobile = db.Column(db.String(11), doc=u'手机号', nullable=False)
    sex = db.Column(db.Integer, doc=u'性别', nullable=False, default=0)
    avatar = db.Column(db.String(128), doc=u'头像', nullable=False)
    is_mobile_auth = db.Column(db.Integer, doc=u'是否通过手机验证', nullable=False)

    create_time = Column("create_time", DATETIME, nullable=False, default=datetime.now, doc=u'创建时间')
    update_time = Column("update_time", DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now,
                         doc=u'更新时间')

    def get_user_info(self, id):
        return db.session.query(
            Customer
        ).filter(
            Customer.id == id
        ).first()


class MobileCodeRecord(db.Model):
    __tablename__ = 't_mobile_code_record'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(64), doc=u'ip', nullable=False)
    mobile = db.Column(db.String(11), doc=u'手机号', nullable=False)
    code = db.Column(db.String(4), doc=u'验证码', nullable=False)
    is_use = db.Column(db.Integer, doc=u'是否被使用 0未使用 1使用', nullable=False, default=0)

    create_time = Column("create_time", DATETIME, nullable=False, default=datetime.now, doc=u'创建时间')
    update_time = Column("update_time", DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now,
                         doc=u'更新时间')


class ArticleCollet(db.Model):
    """
    文章收藏
    """
    __tablename__ = 't_article_collet'
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer)
    uid = db.Column(db.Integer)
    create_time = Column("create_time", DATETIME, nullable=False, default=datetime.now, doc=u'创建时间')
    update_time = Column("update_time", DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now,
                         doc=u'更新时间')


class ArticleComment(db.Model):
    """
    文章评论
    """
    __tablename__ = 't_article_comment'
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer)
    content = db.Column(db.Text)
    commten_type = Column("type", db.Integer, default=0, doc=u'评论类型')
    uid = db.Column(db.Integer,  doc=u'评论用户id')
    comment_id = db.Column(db.Integer, default=0, doc=u'评论id')
    create_time = Column("create_time", DATETIME, nullable=False, default=datetime.now, doc=u'创建时间')
    update_time = Column("update_time", DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now,
                         doc=u'更新时间')

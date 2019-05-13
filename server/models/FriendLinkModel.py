#!/usr/bin/python
# -*- encoding: utf-8 -*-
from server.app import db
from datetime import datetime
from sqlalchemy import DATETIME
from sqlalchemy import Column


# 友情链接
class FriendLink(db.Model):
    __tablename__ = 't_friend_link'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), doc=u'导航名称', nullable=False)
    link_type = db.Column(db.String(10), doc=u"链接类型，pic_link ,text_link")
    link_icon = db.Column(db.String(128), doc=u"导航图标")
    link_href = db.Column(db.String(128), doc=u"导航链接")
    sort = db.Column(db.Integer, doc=u"排序", default=0)
    create_time = Column("create_time", DATETIME, nullable=False, default=datetime.now, doc=u'创建时间')
    update_time = Column("update_time", DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now,
                         doc=u'更新时间')

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "link_type": self.link_type,
            "link_icon": self.link_icon,
            "link_href": self.link_href,
            "sort": self.sort
        }

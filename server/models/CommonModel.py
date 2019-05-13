# -*- coding:utf-8 -*-
from server.app import db
from datetime import datetime
from sqlalchemy import DATETIME
from sqlalchemy import Column


# 系统配置表
class SystemCfg(db.Model):
    __tablename__ = 't_system_cfg'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(32), doc=u'key', unique=True)
    value = db.Column(db.Text, doc=u'value')

    # 添加配置项
    def add_sys_cfg(self, key, value):
        self.key = key
        self.value = value
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            return False
        return True

    # 获取配置值
    def get_sys_value(self, key):
        value = db.session.query(
            SystemCfg.value
        ).filter(SystemCfg.key == key).scalar()
        return value if value else ''

    # 设置配置项
    def set_sys_value(self, key, value):
        cfg = db.session.query(
            SystemCfg
        ).filter(SystemCfg.key == key).scalar()
        if cfg:
            cfg.value = value
            db.session.merge(cfg)
            db.session.commit()
            return True
        else:
            cfg = SystemCfg()
            cfg.key = key
            cfg.value = value
            db.session.add(cfg)
            db.session.commit()
            return True


class BannerCfg(db.Model):
    __tablename__ = 't_banner_cfg'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), doc=u'title')
    href = db.Column(db.String(255), doc=u'href')
    description = db.Column(db.Text, doc=u'description')
    img_url = db.Column(db.String(150), doc=u'img_url')
    sort = db.Column(db.Integer, default=0)
    create_time = Column("create_time", DATETIME, nullable=False, default=datetime.now, doc=u'创建时间')
    update_time = Column("update_time", DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now,
                         doc=u'更新时间')

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "img_url": self.img_url,
            "href": self.href,
            "sort": self.sort
        }

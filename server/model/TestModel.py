#!/usr/bin/python
# -*- encoding: utf-8 -*-
from server.app import db
from datetime import datetime
from sqlalchemy import DATETIME, String
from sqlalchemy import Column


class Teacher(db.Model):
    __tablename__ = 't_teacher'
    id = db.Column(db.Integer, primary_key=True)
    # serial_no = Column('serial_no', String(32), nullable=False, doc=u'唯一序列号')
    name = db.Column(db.String(32), doc=u'名字', nullable=False)
    mobile = db.Column(db.String(32), doc=u'电话', nullable=False)
    create_time = Column("create_time", DATETIME, nullable=False, default=datetime.now, doc=u'创建时间')
    update_time = Column("update_time", DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now,
                         doc=u'更新时间')


class Student(db.Model):
    __tablename__ = 't_student'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer)
    name = db.Column(db.String(32), doc=u'名字', nullable=False)
    mobile = db.Column(db.String(32), doc=u'电话', nullable=False)
    create_time = Column("create_time", DATETIME, nullable=False, default=datetime.now, doc=u'创建时间')
    update_time = Column("update_time", DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now,
                         doc=u'更新时间')

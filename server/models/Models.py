# -*- coding:utf-8 -*-
__author__ = 'kerry'

from server.app import db
from flask_login import UserMixin, AnonymousUserMixin
from server.app import login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
import hashlib

from sqlalchemy import DATETIME
from sqlalchemy import Column

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter(User.id == user_id).first()
    # return User.query.get(user_id)

class User(UserMixin, db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    register_time = db.Column(db.DateTime(), default=datetime.utcnow)
    last_time = db.Column(db.DateTime(), default=datetime.utcnow)
    status = db.Column(db.Boolean, default=True)
    confirmed = db.Column(db.Boolean, default=False)
    nickname = db.Column(db.String(64))

    # 用于外键的字段
    group_id = db.Column(db.Integer, db.ForeignKey('t_user_group.id'))
    group = db.relationship('UsersGroup', backref=db.backref('get_users', lazy='dynamic'))

    create_time = Column("create_time", DATETIME, nullable=False, default=datetime.now, doc=u'创建时间')
    update_time = Column("update_time", DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now, doc=u'更新时间')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "nickname": self.nickname,
            "group_id": self.group_id,
            "create_time": str(self.create_time),
            "update_time": str(self.update_time)
        }


class AnonymousUser(AnonymousUserMixin):
    pass

class UsersGroup(db.Model):
    __tablename__ = 't_user_group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    status = db.Column(db.Integer, default=1)
    rules = db.Column(db.Text())
    description = db.Column(db.Text())
    create_time = Column("create_time", DATETIME, nullable=False, default=datetime.now, doc=u'创建时间')
    update_time = Column("update_time", DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now, doc=u'更新时间')

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "rules": self.rules,
            "create_time": str(self.create_time),
            "update_time": str(self.update_time)
        }

    def __repr__(self):
        return '<UsersGroup>\n' + '\n'.join(['%s:%s' % item for item in self.__dict__.items()])

class MenuAuth(db.Model):
    __tablename__ = 't_menu_auth'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer,default=0)
    name = db.Column(db.String(20))
    method  = db.Column(db.String(50))
    type = db.Column(db.Integer,default=0,doc=u'0基础菜单 1操作和功能')
    sort = db.Column(db.Integer, default=0)
    icon = db.Column(db.String(30))
    is_show = db.Column(db.Integer, default=1)
    create_time = Column("create_time", DATETIME, nullable=False, default=datetime.now, doc=u'创建时间')
    update_time = Column("update_time", DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now, doc=u'更新时间')

    def to_json(self):
        return {
            "id": self.id,
            "parent_id": self.parent_id,
            "name": self.name,
            "method": self.method,
            "type": self.type,
            "sort": self.sort,
            "icon": self.icon,
            "is_show": self.is_show,
            "create_time": str(self.create_time),
            "update_time": str(self.update_time)
        }

    def __repr__(self):
        return '<MenuAuth>\n' + '\n'.join(['%s:%s' % item for item in self.__dict__.items()])


#操作日志
class OperationLog(db.Model):
    __tablename__ = 't_operation_log'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    operation = db.Column(db.String(32))
    operate_desc = db.Column(db.String(1024))
    login_ip = db.Column(db.String(32))
    request = db.Column(db.String(500))
    response = db.Column(db.String(500))
    create_time = Column("create_time", DATETIME, nullable=False, default=datetime.now, doc=u'创建时间')
    update_time = Column("update_time", DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now, doc=u'更新时间')

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "operation": self.operation,
            "operate_desc": self.operate_desc,
            "login_ip":self.login_ip,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S") if self.create_time else '',
        }

    def __repr__(self):
        return '<OperationLog>\n' + '\n'.join(['%s:%s' % item for item in self.__dict__.items()])

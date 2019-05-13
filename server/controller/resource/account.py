#!/usr/bin/python
# -*- encoding: utf-8 -*-
import random
from datetime import datetime, timedelta
import re

from flask import request, session, current_app
from server.app import db
from server.controller.resource import v2, BaseResource

import hashlib

from server.exception import BusinessException, PASSWORD_NOT_MATCH, ERROR, SUCCESS
from server.model.News import Customer, MobileCodeRecord


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
        if user.password != password_md5:
            return self.make_response(ERROR, u'密码不正确')

        session['current_user'] = {
            "uid": user.id
        }
        return self.make_response(SUCCESS, u"登录成功")


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

        resp = self._post(current_app.config.get('MSG_URL'), para, headers)

        # if resp['code'] != '000000':
        #     return self.make_response(ERROR, u'短信发送失败')

        mobile_record = MobileCodeRecord()
        mobile_record.mobile = mobile
        mobile_record.ip = ip
        mobile_record.code = secucode
        db.session.add(mobile_record)
        db.session.commit()
        return self.make_response(ERROR, u'发送成功')


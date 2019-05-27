# -*- coding:utf-8 -*-
from datetime import timedelta


class Config:
    DEBUG = False
    CONFIG_NAME = 'default'
    SECRET_KEY = '\x03d\xf4\x95J\x15\xa4B\xfb\xc0\xaf \xd1A[j$}\x18\x16a\xe7\xd0\xec'
    STRIPE_API_KEY = '\x03d\xf4\x95J\x15\xa4B\xfb\xc0\xaf \xd1A[j$}\x18\x16a\xe7\xd0\xec'
    PAGE_SIZE = 15
    SQLALCHEMY_ECHO = False
    VERSION = '1.0.1'
    LOG_FILE = 'info.log'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    # app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!

    # 日志配置项
    LOG_FILE_MAX_SIZE = 1024 * 5 * 1000
    LOG_FILE_NUM_BACKUPS = 5

    # 邮件配置
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = '1509699669@qq.com'
    MAIL_PASSWORD = 'tkmhowtztlltbagf'

    # jwt配置
    JWT_SECRET_KEY = 'tkmhowtztlltbagf11212'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=30)
    JWT_HEADER_NAME = 'Authorization'
    # JWT_REFRESH_JSON_KEY = 'refresh_token'

    JWT_HEADER_TYPE = ''
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # 短信配置
    SID = '42f6ac4992866c8b69b18cfcc8b224ae'
    TOKEN = '95eeabcfc4865a1b7aea38f0a8bcdcea'
    APPID = '4e5ff31bfc5d4190a7225d113289a3ef'
    TEMPLATE_ID = '312050'
    MSG_URL = 'https://open.ucpaas.com/ol/sms/sendsms'

    # 所有SQLALCHEMY配置项可参考手册http://www.pythondoc.com/flask-sqlalchemy/config.html#id2
    @staticmethod
    def init_app(app):
        pass


class LocalConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Bitnow2018@47.74.251.5/36k?charset=utf8"


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1/36k?charset=utf8"


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'local': LocalConfig
}

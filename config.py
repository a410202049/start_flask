# -*- coding:utf-8 -*-


class Config:
    DEBUG = True
    CONFIG_NAME = 'default'
    SECRET_KEY = '\x03d\xf4\x95J\x15\xa4B\xfb\xc0\xaf \xd1A[j$}\x18\x16a\xe7\xd0\xec'
    STRIPE_API_KEY = '\x03d\xf4\x95J\x15\xa4B\xfb\xc0\xaf \xd1A[j$}\x18\x16a\xe7\xd0\xec'
    PAGE_SIZE = 15
    SQLALCHEMY_ECHO = False
    VERSION = '1.0.1'

    # 所有SQLALCHEMY配置项可参考手册http://www.pythondoc.com/flask-sqlalchemy/config.html#id2
    @staticmethod
    def init_app(app):
        pass


class LocalConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Bitnow2018@47.74.251.5/test_123?charset=utf8"


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'local': LocalConfig
}

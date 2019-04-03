# coding: utf-8
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy

from config import config
from werkzeug.utils import import_string
import sys

from server.exception import ServerBaseException
from server.util.log import FinalLogger

from flask_mail import Message
from flask_mail import Mail
from flask_restplus import Api


reload(sys)
sys.setdefaultencoding("utf-8")

# 设置db.session.query 可以使用分页类
session_options = {}
# session_options['query_cls'] = BaseQuery
session_options['autocommit'] = False
session_options['autoflush'] = False
session_options['expire_on_commit'] = False

db = SQLAlchemy(session_options=session_options)


# jinja2 None to ''
def finalize(arg):
    if arg is None:
        return ''
    return arg


def register_blueprints(app):
    # 注册蓝图
    blueprints = [
        "server.controller.home:home"
    ]
    for bp_name in blueprints:
        bp = import_string(bp_name)
        app.register_blueprint(bp)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    # 开启调试模式
    app.debug = app.config.get('DEBUG')

    # jinja2 None to ''
    app.jinja_env.finalize = finalize

    from server import template_filter
    template_filter.init_app(app)

    # 初始化路由
    import routing
    routing.init_routing(app)

    # 注册蓝图
    register_blueprints(app)

    # 初始化日志类
    logger = FinalLogger(app).get_logger()

    # 初始化邮件
    mail = Mail()
    mail.init_app(app)

    # 初始化 restplus
    api = Api(app)
    from server.controller.resource import init_api
    init_api(api)

    def send_email(title, body):
        msg = Message(title, sender='1509699669@qq.com', recipients=['1509699669@qq.com'])
        msg.body = body
        with app.app_context():
            mail.send(msg)

    @app.after_request
    def after_request(response):
        pass
        # for query in get_debug_queries():
        #     if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
        #         current_app.logger.warning(
        #             'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
        #             % (query.statement, query.parameters, query.duration,
        #                query.context))
        return response

    @app.errorhandler(Exception)
    def handle_exception(e):
        # if current_app.config['CONFIG_NAME'] != 'local':
        if not isinstance(e, ServerBaseException):
            logger.exception(u'service has exception: {0}'.format(e.message))
            import traceback
            logger.info(u'Server异常: \n{message}'.format(message=traceback.format_exc()))
            import gevent
            from gevent import Greenlet, monkey
            monkey.patch_all()

            title = u'server 异常处理'
            body = u'Server异常: \n{message}'.format(message=traceback.format_exc())

            gevent.joinall([
                # 这里spawn是3个任务[实际是3个协程]，每个任务都会执行fetch_async函数
                gevent.spawn(send_email, title, body)

            ])
            raise e
        return e.error_msg
    return app
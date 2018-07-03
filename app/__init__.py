"""
register flask app object
"""
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()
mail = Mail()

from app.models.base import db


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object('app.config.secure')
    app.config.from_object('app.config.setting')
    register_blueprint(app)

    init_loginmanager_app(app)

    # 初始化mail插件
    mail.init_app(app)

    # 创建所有数据库映射
    db.init_app(app)

    # 防止create_all异常的三种方法:
    # 一: app= 传入创建的app对象
    #    db.create_all(app=app)
    # 二: 使用上下文管理器将当前app对象推入栈顶
    with app.app_context():
        db.create_all()
    # 三: 在使用SQLAlchemy()实例化SQLAlchemy对象时传入app关键词参数
    return app


def init_loginmanager_app(app):
    # 初始化login_manager插件
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'


def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)

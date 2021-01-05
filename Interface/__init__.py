from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Config import config
from flask_cors import *
from .utils.nestable_blueprint import NestableBlueprint

db = SQLAlchemy()


# 创建APP
def create_app(config_name):
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_object(config[config_name])
    # 注册数据库链接
    db.init_app(app)
    # 注册蓝图
    register_blueprint(app)

    return app


# 注册蓝图
def register_blueprint(app):
    # 获取到API文档的嵌套蓝图
    from .api import create_api
    api_v1 = create_api()
    # 把蓝图注册到主线程
    app.register_blueprint(api_v1)

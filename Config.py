# _*_ coding: utf-8 _*_
import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:bluese0712.@localhost:3306/info_management?charset=utf8'
    # Session加密
    SECRET_KEY = 'E19FAB00ED9D9E89137D2FF7C4605C14'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    JSON_AS_ASCII = False
    # 项目定义
    # 上传文件保存总路径
    UPLOAD_FOLDER_SAVE = './app/upload_file'
    # 上传文件保存至数据库时总路径
    UPLOAD_FOLDER_SQL = '/upload_file'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:bluese0712.@localhost:3306/info_management?charset=utf8'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    "testing": TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

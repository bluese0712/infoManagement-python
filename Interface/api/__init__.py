from flask import Blueprint
from Interface.utils.nestable_blueprint import NestableBlueprint
# 一级蓝图路由指向API
api = Blueprint('api', __name__, url_prefix='')
# 二级蓝图路由指向具体功能
cw_record_api = Blueprint('cw_record', __name__, url_prefix='/cw/record')
cw_category_api = Blueprint('cw_category', __name__, url_prefix='/cw/category')

# 引入具体API文件
# from . import user, common, realm_name, mailbox, mailbox_group, department, recipient, recipient_group, mail_template
from .finance import record, category


def create_api():
    api_v1 = NestableBlueprint('api_v1', __name__, url_prefix='/api')

    api_v1.register_blueprint(api)
    api_v1.register_blueprint(cw_record_api)
    api_v1.register_blueprint(cw_category_api)

    return api_v1

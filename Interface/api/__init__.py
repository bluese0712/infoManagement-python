from flask import Blueprint
from Interface.utils.nestable_blueprint import NestableBlueprint
# 一级蓝图路由指向API
api = Blueprint('api', __name__, url_prefix='')
# 二级蓝图路由指向具体功能
user_api = Blueprint('user', __name__, url_prefix='/user')

cw_record_api = Blueprint('cw_record', __name__, url_prefix='/cw/record')
cw_category_api = Blueprint('cw_category', __name__, url_prefix='/cw/category')
cw_fund_api = Blueprint('cw_fund', __name__, url_prefix='/cw/fund')

# 引入具体API文件
# from . import user, common, realm_name, mailbox, mailbox_group, department, recipient, recipient_group, mail_template
from . import user, common
from .finance import record, category, fund


def create_api():
    api_v1 = NestableBlueprint('api_v1', __name__, url_prefix='/api')

    api_v1.register_blueprint(api)
    api_v1.register_blueprint(user_api)

    api_v1.register_blueprint(cw_record_api)
    api_v1.register_blueprint(cw_category_api)
    api_v1.register_blueprint(cw_fund_api)

    return api_v1

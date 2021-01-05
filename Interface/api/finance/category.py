from Interface.api import cw_category_api
from flask import request, session
from Interface.utils import is_login, Success, Fail, return_json, form_has_parameter as validate
from Interface.models import CWCategory


# 根据条件获取财务记录列表
@cw_category_api.route('/getCategoryListByParams', methods=['POST'])
# @is_login
def get_category_by_params():
    param = [CWCategory.deleteStatus == 0]
    department_list = CWCategory.to_paginate_dict(CWCategory.query.filter(*param).order_by(CWCategory.categoryID),
                                                  int(request.form.get('pageNumber', 1)),
                                                  int(request.form.get('pageSize', 20)))
    return return_json(Success(data=department_list))


# 创建财务记录
@cw_category_api.route('/createCategory', methods=['POST'])
# @is_login
def create_category():
    required = validate(request.form, [{'categoryID': '所属类型为空'}, {'amount': '金额为空'}, {'dissipate': '消费时间为空'}])
    if required:
        return return_json(Fail(msg=required))
    record = CWCategory(categoryID=request.form.get('categoryID'), amount=request.form.get('amount'),
                      dissipate=request.form.get('dissipate'),
                      userID=session.get(request.cookies.get("SESSIONID")).get('userID'))
    return return_json(Success(msg='添加成功') if CWCategory.to_add(record) else Fail(msg='添加失败'))

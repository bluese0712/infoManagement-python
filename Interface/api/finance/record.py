from Interface.api import cw_record_api
from flask import request, session
from Interface.utils import is_login, Success, Fail, return_json, form_has_parameter as validate, date_string_to_date
from Interface.models import CWRecord


# 根据条件获取财务记录列表
@cw_record_api.route('/getRecordListByParams', methods=['POST'])
@is_login
def get_record_by_params():
    param = [CWRecord.deleteStatus == 0]
    if request.form.get('startTime'):
        param.append(CWRecord.dissipate >= date_string_to_date(request.form.get('startTime'), '%Y-%m-%d %H:%M:%S'))
    if request.form.get('endTime'):
        param.append(CWRecord.dissipate <= date_string_to_date(request.form.get('endTime'), '%Y-%m-%d %H:%M:%S'))
    if request.form.get('categoryID'):
        param.append(CWRecord.categoryID == request.form.get('categoryID'))
    department_list = CWRecord.to_paginate_dict(CWRecord.query.filter(*param).order_by(CWRecord.dissipate.desc()),
                                                int(request.form.get('pageCurrent', 1)),
                                                int(request.form.get('pageSize', 20)))
    return return_json(Success(data=department_list))


# 创建财务记录
@cw_record_api.route('/createRecord', methods=['POST'])
@is_login
def create_record():
    required = validate(request.form, [{'categoryID': '所属类型为空'}, {'amount': '金额为空'}, {'dissipate': '消费时间为空'}])
    if required:
        return return_json(Fail(msg=required))
    record = CWRecord(categoryID=request.form.get('categoryID'), amount=request.form.get('amount'),
                      dissipate=date_string_to_date(request.form.get('dissipate'), '%Y-%m-%d %H:%M:%S'),
                      userID=session.get(request.cookies.get("BLUE_FEATHER_SESSION")).get('userID'))
    return return_json(Success(msg='添加成功') if CWRecord.to_add(record) else Fail(msg='添加失败'))


# 编辑财务记录
@cw_record_api.route('/editRecord', methods=['POST'])
@is_login
def edit_record():
    required = validate(request.form, [{'recordID': '记录ID为空'}, {'amount': '金额为空'}, {'dissipate': '消费时间为空'}])
    if required:
        return return_json(Fail(msg=required))
    record = CWRecord.query.get(request.form.get('recordID'))
    if not record:
        return return_json(Fail(msg='记录ID错误'))
    if record.userID != session.get(request.cookies.get("BLUE_FEATHER_SESSION")).get('userID'):
        return return_json(Fail(msg='用户无权修改'))
    record.dissipate = date_string_to_date(request.form.get('dissipate'), '%Y-%m-%d %H:%M:%S')
    record.amount = request.form.get('amount')
    return return_json(Success(msg='添加成功') if CWRecord.to_update() else Fail(msg='添加失败'))


# 删除财务记录
@cw_record_api.route('/deleteRecord', methods=['POST'])
@is_login
def delete_record():
    required = validate(request.form, [{'recordID': '记录ID为空'}])
    if required:
        return return_json(Fail(msg=required))
    record = CWRecord.query.get(request.form.get('recordID'))
    if not record:
        return return_json(Fail(msg='记录ID错误'))
    if record.userID != session.get(request.cookies.get("BLUE_FEATHER_SESSION")).get('userID'):
        return return_json(Fail(msg='用户无权修改'))
    return return_json(Success(msg='添加成功') if CWRecord.to_delete(record) else Fail(msg='添加失败'))
from . import department_api
from flask import request, session
from Interface.utils import is_login, Success, Fail, return_json, form_has_parameter as validate
from Interface.models import Department, update_department


# 根据条件获取组织列表
@department_api.route('/getDepartmentListByParams', methods=['POST'])
@is_login
def get_department_by_params():
    param = [Department.forbidStatus == 0]
    if request.form.get('departmentName'):
        param.append(Department.departmentName.like("%"+request.form.get('department')+"%"))
    department_list = Department.to_paginate_dict(Department.query.filter(*param).order_by(Department.departmentID),
                                                  int(request.form.get('pageNumber', 1)),
                                                  int(request.form.get('pageSize', 20)))
    return return_json(Success(data=department_list))


# 创建组织
@department_api.route('/createDepartment', methods=['POST'])
@is_login
def create_department():
    required = validate(request.form, [{'departmentName': '部门名称为空'}, {'sendingPriority': '发送优先度为空'}])
    if required:
        return return_json(Fail(msg=required))
    if request.form.get('parentID'):
        parent = Department.query.get(request.form.get('parentID'))
        if not parent:
            return return_json(Fail(msg='父节点ID错误'))
    department = Department(departmentName=request.form.get('departmentName'), parentID=request.form.get('parentID'),
                            sendingPriority=request.form.get('sendingPriority'),
                            creatorID=session.get(request.cookies.get("SESSIONID")).get('userID'))
    return return_json(Success(msg='添加成功') if Department.to_add(department) else Fail(msg='添加失败'))


# 删除组织
@department_api.route('/deleteDepartment', methods=['POST'])
@is_login
def delete_department():
    if not request.form.get('departmentID'):
        return return_json(Fail(msg='组织ID为空'))
    realm_name = Department.query.get(request.form.get('departmentID'))
    if not realm_name:
        return return_json(Fail(msg='组织ID错误'))
    return return_json(Success(msg='删除成功') if Department.to_delete(realm_name) else Fail(msg='删除失败'))


# 编辑组织
@department_api.route('/editDepartment', methods=['POST'])
@is_login
def edit_department():
    if not request.form.get('departmentID'):
        return return_json(Fail(msg='组织ID为空'))
    elif not request.form.get('departmentName'):
        return return_json(Fail(msg='组织名称为空'))
    department = Department.query.get(request.form.get('departmentID'))
    if not department:
        return return_json(Fail(msg='组织ID错误'))
    return return_json(Success(msg='编辑成功')
                       if update_department(department, request.form.get('departmentName')) else Fail(msg='编辑失败'))


# 获取所有可用组织
@department_api.route('/getAllDepartmentList', methods=['POST'])
@is_login
def get_all_department_list():
    realm_name_list = Department.query.filter(Department.forbidStatus == 0).all()
    return return_json(Success(data=[item.to_dict() for item in realm_name_list]))

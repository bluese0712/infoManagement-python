import hashlib
from . import user_api
from flask import request, session
from Interface.utils import is_login, Success, Fail, return_json, form_has_parameter as validate
from Interface.models import User


# 根据条件获取用户列表
@user_api.route('/getUserListByParams', methods=['POST'])
@is_login
def get_user_by_params():
    param = [User.deleteStatus == 0]
    if request.form.get('userName'):
        param.append(User.userName.like("%"+request.form.get('userName')+"%"))
    if request.form.get('nickName'):
        param.append(User.nickName.like("%"+request.form.get('nickName')+"%"))
    users = User.to_paginate_dict(User.query.filter(*param), int(request.form.get('pageNumber', 1)),
                                  int(request.form.get('pageSize', 20)))
    print(session.get(request.cookies.get("BLUE_FEATHER_SESSION")))
    return return_json(Success(data=users))


# 创建用户
@user_api.route('/createUser', methods=['POST'])
@is_login
def create_user():
    required = validate(request.form, [{'userName': '用户名为空'}, {'nickName': '昵称为空'}, {'password': '密码为空'}])
    if required:
        return return_json(Fail(msg=required))

    user_list = User.query.filter(User.userName == request.form.get('userName')).all()
    if len(user_list) != 0:
        return return_json(Fail(msg='用户名重复'))
    user = User(userName=request.form.get('userName'), nickName=request.form.get('nickName'),
                password=hashlib.md5(bytes(request.form.get('password'), encoding="utf8")).hexdigest().upper(),
                creatorID=session.get(request.cookies.get("BLUE_FEATHER_SESSION")).get('userID'))
    return return_json(Success(msg='添加成功') if User.to_add(user) else Fail(msg='添加失败'))


# 删除用户
@user_api.route('/deleteUser', methods=['POST'])
@is_login
def delete_user():
    if not request.form.get('userID'):
        return return_json(Fail(msg='角色ID为空'))
    user = User.query.get(request.form.get('userID'))
    if not user:
        return return_json(Fail(msg='角色ID错误'))
    return return_json(Success(msg='删除成功') if User.to_delete(user) else Fail(msg='删除失败'))

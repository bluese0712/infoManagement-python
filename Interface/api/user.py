import hashlib
from . import user_api
from Interface.utils.utils import is_login
from flask import request
from Interface.utils.return_status import Success, Fail, return_json
from Interface.models import User


# 根据条件获取用户列表
@user_api.route('/getUserListByParams', methods=['POST'])
@is_login
def get_user_by_params():
    page_size = int(request.form.get('pageSize', 20))
    page_number = int(request.form.get('pageNumber', 1))
    param = [User.forbidStatus == 0]
    if request.form.get('username'):
        param.append(User.username.like("%"+request.form.get('username')+"%"))
    users = User.to_paginate_dict(User.query.filter(*param).order_by(User.userID), page_number, page_size)
    return return_json(Success(data=users))


# 创建用户
@user_api.route('/createUser', methods=['POST'])
@is_login
def create_user():
    if not request.form.get('username'):
        return return_json(Fail(msg='角色名为空'))
    elif not request.form.get('password'):
        return return_json(Fail(msg='密码为空'))
    user = User(username=request.form.get('username'),
                password=hashlib.md5(bytes(request.form.get('password'), encoding="utf8")).hexdigest().upper())
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

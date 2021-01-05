from flask import jsonify


# 基础数据类型
class Basics:
    code = 0
    result = ''
    msg = ''
    data = None


# 成功 200
class Success(Basics):
    code = 200
    result = 'success'

    def __init__(self, code=code, result=result, msg=Basics.msg, data=Basics.data):
        self.code = code
        self.result = result
        self.msg = msg
        self.data = data


# 报错 401
class Fail(Basics):
    code = 401
    result = 'fail'

    def __init__(self, code=code, result=result, msg=Basics.msg, data=Basics.data):
        self.code = code
        self.result = result
        self.msg = msg
        self.data = data


# 系统异常报错 400
class SystemFail(Basics):
    code = 400
    result = 'fail'
    msg = '系统内部异常'


# 用户令牌过期报错 901
class UserTokenFail(Basics):
    code = 901
    result = 'fail'
    msg = '用户令牌已过期，请重新登陆'


# 用户未登录 902
class UserNoLoginFail(Basics):
    code = 902
    result = 'fail'
    msg = '用户未登录'


def return_json(message: Basics):
    return jsonify({'msg': message.msg, 'result': message.result, 'code': message.code, 'data': message.data})

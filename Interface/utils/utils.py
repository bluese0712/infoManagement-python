import uuid, functools
from datetime import datetime
from flask import request, session
from Interface.utils import return_json, UserTokenFail, UserNoLoginFail


# 生成大写的UUID
def uuid_32_upper():
    return ''.join(str(uuid.uuid4()).split('-')).upper()


# 是否登录
def is_login(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        session_id = request.cookies.get("SESSIONID")
        if not session_id:
            return return_json(UserNoLoginFail)
        user = session.get(session_id)
        if not user:
            return return_json(UserTokenFail)
        return func(*args, **kwargs)
    return inner


# 时间按指定格式转换成Python时间
def date_string_to_date(date_string, format_):
    try:
        date = datetime.strptime(date_string, format_)
    except Exception as e:
        print(e)
        return None
    return date


# 判断参数是否存在
def form_has_parameter(form: dict, array: list):
    for field in array:
        key = sorted(field.keys())[0]
        val = form.get(key, None)
        if not val:
            return field[key]
    return None

import hashlib
from . import api
from app.utils.utils import uuid_32_upper
from app.utils.rsa_key import get_public_rsa, decrypt_by_private_key
from flask import request, session, make_response
from app.utils.return_status import Success, Fail, return_json
from app.models import User


# 登录
@api.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    pwd_http = decrypt_by_private_key(password)
    if not pwd_http:
        return return_json(Fail(msg='密码错误'))
    pwd = hashlib.md5(bytes(pwd_http, encoding="utf8")).hexdigest().upper()
    users = User.query.filter_by(username=username).all()
    for user in users:
        if user.password == pwd and user.forbidStatus:
            return return_json(Fail(msg='用户已失效'))
        if user.password == pwd:
            session_id = uuid_32_upper()
            resp = make_response(return_json(Success(data=User.to_dict(user))))
            resp.set_cookie('SESSIONID', session_id, max_age=60 * 60 * 24 * 3)
            session[session_id] = User.to_dict(user)
            return resp
    return return_json(Fail(msg='密码错误'))


# 获取RSA公钥
@api.route('/getRSAPublicKey', methods=['GET'])
def get_res_public_key():
    return return_json(Success(data=get_public_rsa()))


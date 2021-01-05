import base64, json, redis, hashlib
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

r = redis.StrictRedis(host='localhost', port=6379, db=0)


# 创建RAS密钥对并返回公钥
def create_rsa():
    # 生成RSA秘钥
    key = RSA.generate(1024)
    # 获取私钥
    private_key = str(key.export_key(), encoding='utf-8')
    # 保存私钥至Redis
    r.set(hashlib.md5(b'cheat_email_RSA_private_key').hexdigest().upper(), private_key)
    # 获取公钥
    public_key = str(key.publickey().export_key(), encoding='utf-8')
    # 保存公钥至Redis
    r.set(hashlib.md5(b'cheatEmailRSAPublicKey').hexdigest().upper(), public_key)
    r.set(hashlib.md5(b'cheatEmailRSACreate').hexdigest().upper(), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # 返回公钥
    return public_key


# 从Redis中获取公钥
def get_public_rsa():
    t = r.get(hashlib.md5(b'cheatEmailRSACreate').hexdigest().upper())
    if not t:
        return create_rsa()
    t_str = str(r.get(hashlib.md5(b'cheatEmailRSACreate').hexdigest().upper()), encoding='utf-8')
    if datetime.strptime(t_str, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d') != datetime.now().strftime('%Y-%m-%d'):
        return create_rsa()

    value = r.get(hashlib.md5(b'cheatEmailRSAPublicKey').hexdigest().upper())
    if value and type(value) == bytes:
        return str(value, encoding='utf-8')
    elif value:
        return value
    return create_rsa()


# 解密
def decrypt_by_private_key(date):
    key = r.get(hashlib.md5(b'cheat_email_RSA_private_key').hexdigest().upper())
    private_key = PKCS1_v1_5.new(RSA.importKey(key))
    decrypt_text = private_key.decrypt(base64.b64decode(date), None)
    if not decrypt_text:
        return None
    pwd_json = json.loads(decrypt_text)
    t = pwd_json.get('encryptionTime')
    if (not t) or datetime.strptime(t, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d') \
            != datetime.now().strftime('%Y-%m-%d'):
        return None
    return pwd_json.get('password')

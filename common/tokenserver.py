# @Author  : kane.zhu
# @Time    : 2020/6/13 19:42
# @Software: PyCharm

import time
from django.core import signing
import hashlib
from django.core.cache import cache




KEY = 'bWlkcGxhdGZvcm0gYXV0aA'
SALT = 'bWlkcGxhdGZvcm0g'
TIME_OUT = 30 * 60  # 30min
TIME_OUT_REFRESH = 30 * 60 * 60  # 30min


def encrypt(obj):
    """加密"""
    value = signing.dumps(obj, key=KEY, salt=SALT)
    value = signing.b64_encode(value.encode()).decode()
    return value


def decrypt(src):
    """解密"""
    src = signing.b64_decode(src.encode()).decode()
    raw = signing.loads(src, key=KEY, salt=SALT)
    print(type(raw))
    return raw


def create_token(username):
    """生成token信息"""
    # 1. 加密头信息
    # import calendar
    # import time
    # header = encrypt(str(calendar.timegm(time.gmtime())))
    # 2. 构造Payload
    payload = {"username": username, "iat": time.time()}
    payloadRefresh = {"username": username, "refresh_token": time.time() + 1800}
    payload = encrypt(payload)
    payloadRefresh = encrypt(payloadRefresh)
    # 3. 生成签名
    md5 = hashlib.md5()
    md5.update(("%s" % ( payload)).encode())
    signature = md5.hexdigest()
    token = "%s.%s" % ( payload, signature)
    refresh_token = "%s.%s" % ( payloadRefresh, signature)
    # 存储到缓存中
    from common import  checklogin
    checklogin.redisOps(k=username+'_token',v=token,expire=TIME_OUT)
    checklogin.redisOps(k=username+'_refresh_token',v=refresh_token,expire=TIME_OUT_REFRESH)

    return token,refresh_token

# @Author  : kane.zhu
# @Time    : 2020/6/13 19:42
# @Software: PyCharm
from django.http import JsonResponse
from common import baseconfig
TIME_OUT = baseconfig.getconfig()['redisToeknExpire'].rstrip()
import re
TIME_OUT = int(re.sub("\D", "", TIME_OUT))

from common import checklogin
from midplatform import settings


def isLogin(func):
    def inner(request,*args,**kwargs):
        token=request.META.get('HTTP_AUTHORIZATION')
        if token is None or checklogin.keyExists(token) == 0:
            settings.finalData['code'] = 2005
            settings.finalData['msg'] = settings.codeMsg[2005]
            return JsonResponse(settings.finalData)
        else:
            print(checklogin.keyExists(token))
            return func(*args,**kwargs)
    return inner


import itsdangerous
salt = baseconfig.getconfig()['tokensalt']

def create_token(username):
    t = itsdangerous.TimedJSONWebSignatureSerializer(salt,expires_in=TIME_OUT)
    res = t.dumps({'username':username})
    token = res.decode()

    checklogin.keyset(k=token, v=username, expire=TIME_OUT)
    return  token

def get_token(token):
    t = itsdangerous.TimedJSONWebSignatureSerializer(salt, expires_in=TIME_OUT)
    user = t.loads(token)
    return user





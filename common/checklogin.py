# @Author  : kane.zhu
# @Time    : 2020/6/15 19:13
# @Software: PyCharm
import redis
from common import baseconfig
redishost= baseconfig.getconfig()['redisAddr']
redisPort= int(baseconfig.getconfig()['redisPort'])
redisPass= baseconfig.getconfig()['redisPass']
r = redis.Redis(host=redishost, port=redisPort, decode_responses=True, password=redisPass)

def keyset(**tokenserials):
    r.set(tokenserials['k'],tokenserials['v'],tokenserials['expire'])

def keyExists(key):
    """
    :param key: 登陆后得到的KEY
    :return: int 0 不存在 1 存在
    """
    res= r.exists(key)
    return res


def getNameByToken(key):
    res= r.get(key)
    resdata= res.split('|')[0]
    return  resdata



# 用于登出 去清理token
def clearToken(key):
    respdata = r.get(key).split('|')[0]
    res= r.delete(key)
    return  respdata

def getTranceIdByToken(key):
    # 根据token 获取traceID
    res= r.get(key).split('|')[1]
    return  res


FLAG = False
def is_login(func):
    def inner(*args,**kwargs):
        print(*args,**kwargs)
        global FLAG
        if FLAG:
            ret = func(*args,**kwargs)
            return  ret

        else:
            print('dd')
            # keyExists(key)

    return inner
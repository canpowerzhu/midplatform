# @Author  : kane.zhu
# @Time    : 2020/6/15 19:13
# @Software: PyCharm

def redisOps(**tokenserials):
    print(tokenserials)
    import redis
    r = redis.Redis(host='192.168.1.5', port=8006, decode_responses=True,password='**')
    r.set(tokenserials['k'],tokenserials['v'],tokenserials['expire'])


def checklogin():
    pass

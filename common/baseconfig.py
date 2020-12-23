# @Author  : kane.zhu
# @Time    : 2020/6/17 20:54
# @Software: PyCharm

from sysconf import models


def getconfig():
    configs = models.baseConfig.objects.all().values_list('confKey','confValue')
    configDic={}
    for kv in list(configs):
        configDic[kv[0]]=kv[1]

    return configDic



def getnickname(id):
    nickname = models.sys_user.objects.filter(pk=id).values('nickname').first()['nickname']
    # print(nickname)
    return nickname

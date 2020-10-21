# @Author  : kane.zhu
# @Time    : 2020/9/24 16:33
# @Software: PyCharm

from component import models as logmodels

operateType={
    0:"增加",
    1:"删除",
    2:"修改"
}


def logrecord(type, request, data):
    if 'HTTP_X_FORWARDED_FOR' in request.META.keys():
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']

    import datetime, json
    from common import checklogin

    BroswerType = request.user_agent.browser.family

    BroswerVersion = ".".join(str(i) for i in list(request.user_agent.browser.version))

    if request.body.decode('utf-8'):
        reqBody = json.loads(request.body.decode('utf-8'))
    else:
        reqBody = None

    if type == 0:
        # 登陆登出相关
        operateUser = data['username']
        if data['status'] == 0:
            # 成功
            actionstatus = 0
        else:
            # 失败
            actionstatus = 1

        if data['action'] == 0:
            # 登出
            loginaction = 0
        else:
            # 登入
            loginaction = 1

        logmodels.login_out.objects.create(traceId=data['traceId'],
                                           username=operateUser,
                                           status=actionstatus,
                                           ipAdress=ip.split(',')[1],
                                           osType=request.META['OS'],
                                           broswerType=BroswerType,
                                           broswerVersion=BroswerVersion,
                                           userAgent=request.META['HTTP_USER_AGENT'],
                                           action=loginaction,
                                           requestTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    else:
        operateUser = (checklogin.getNameByToken(request.META['HTTP_AUTHORIZATION']))
        traceId = (checklogin.getTranceIdByToken(request.META['HTTP_AUTHORIZATION']))
        logmodels.operatelog.objects.create(traceId=traceId,
                                            username=operateUser,
                                            protocol=request.META['SERVER_PROTOCOL'],
                                            path=request.get_full_path(),
                                            msg=data['msg'],
                                            status=1,
                                            method=request.method,
                                            ipAdress=ip.split(',')[1],
                                            params=reqBody,
                                            requestTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    return True

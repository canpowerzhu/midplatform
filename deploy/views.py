from django.shortcuts import render, HttpResponse, HttpResponseRedirect
import json
import requests
from deploy import models
from django.conf import settings
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core.paginator import Paginator

import datetime


##发布记录包含四个接口： addrecord、editrecord、getallrecord
#
#
def getallrecord(request):
    limit = int(request.GET.get('limit', default=10))
    page = int(request.GET.get('page', default=1))

    projectName = request.GET.get('projectName')
    publisher = request.GET.get('publisher')

    kwargs = {
        # 动态查询的字段
    }
    if publisher != None and projectName != None:
        kwargs['publisher'] = publisher
        kwargs['projectName'] = projectName

    elif projectName != None:
        kwargs['projectName'] = projectName

    elif publisher != None:
        kwargs['Publisher'] = publisher
    else:
        count = models.deployRecord.objects.filter(**kwargs).count()
        res = models.deployRecord.objects.filter(**kwargs).order_by('-deployTime').values()

    count = models.deployRecord.objects.filter(**kwargs).count()
    res = models.deployRecord.objects.filter(**kwargs).order_by('-deployTime').values()

    # 每页显示10条记录
    paginator = Paginator(res, limit)
    # 获取第2页的数据
    pageData = paginator.page(page)
    datalist = list(pageData)
    if count > 0:
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        settings.RESULT['count'] = count
        settings.RESULT['data'] = datalist
    else:
        settings.RESULT['code'] = 2002
        settings.RESULT['msg'] = "fail"
    return JsonResponse(settings.RESULT)


def addrecord(request):
    if request.method == 'POST':
        res = json.loads(request.body.decode('utf-8'))
        from sysconf import models as  sysmol
        testname = sysmol.sys_user.objects.filter(id=res['tester']).values('nickname').first()['nickname']

        # TODO 没有缓存上传为0 需要判断
        # {'isModifyCache': 0, 'isModifySql': 0, 'projectName': '21212121', 'state': 0, 'isRollBack': 1, 'publisher': 'dixiaoping', 'modifyContent': '11212211221', 'modifyModel': '21233232122112'}
        kwargs = {
            ##动态参数
        }
        if res['isModifyCache'] == 1:
            kwargs['isModifyCache'] = 1
            kwargs['cacheDetail'] = res['cacheDetail']

        if res['isModifySql'] == 1:
            kwargs['isModifySql'] = 1
            kwargs['sqlDetail'] = res['sqlDetail']

        kwargs['projectName'] = res['projectName']
        kwargs['isRollBack'] = res['isRollBack']
        kwargs['modifyModel'] = res['modifyModel']
        kwargs['modifyContent'] = res['modifyContent']
        kwargs['tester'] = testname
        kwargs['state'] = 0
        kwargs['publisher'] = res['publisher']

        models.deployRecord.objects.create(**kwargs)
        front_respone = {'code': 2001, 'msg': None}
        front_respone['msg'] = 'success'
        res['tester'] = testname
        dingtalkmsg(res, 0)
        return JsonResponse(front_respone)


def editrecord(request):
    ###这里进行修改step状态
    kwargs = {

    }

    front_respone = {'code': 2001, 'msg': None}
    if request.method == 'POST':
        res = json.loads(request.body.decode('utf-8'))
        stepinfo = int(res['status'])
    finishTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    ###测试步骤
    kwargs['step'] = int(res['step']) + 1
    if stepinfo == 1 or stepinfo == 2:
        kwargs['state'] = 1
        kwargs['testStatus'] = res['status']
        kwargs['testResult'] = res['Result']
        if stepinfo == 1:
            kwargs['state'] = 2
            kwargs['finishTime'] = finishTime
            kwargs['elapsedTime'] = proTime(res)
    ### 审核步骤
    if stepinfo == 3 or stepinfo == 4:
        kwargs['state'] = 1
        kwargs['aduitStatus'] = res['status']
        kwargs['aduitResult'] = res['Result']
        if stepinfo == 3:
            kwargs['state'] = 2
            kwargs['finishTime'] = finishTime
            kwargs['elapsedTime'] = proTime(res)

    ### 部署步骤
    if stepinfo == 5 or stepinfo == 6:
        kwargs['state'] = 1
        kwargs['arrangeStatus'] = res['status']
        kwargs['arrangeResult'] = res['Result']
        if stepinfo == 5:
            kwargs['state'] = 2
            kwargs['finishTime'] = finishTime
            kwargs['elapsedTime'] = proTime(res)

    ### 发布步骤
    if stepinfo == 7 or stepinfo == 8:
        kwargs['state'] = 1
        kwargs['deployStatus'] = res['status']
        kwargs['deployResult'] = res['Result']
        kwargs['state'] = 2
        if stepinfo == 7:
            kwargs['state'] = 2
            kwargs['finishTime'] = finishTime
            kwargs['elapsedTime'] = proTime(res)

    models.deployRecord.objects.filter(pk=res['id']).update(**kwargs)
    data = model_to_dict(models.deployRecord.objects.get(pk=res['id']))
    print(data)
    dingtalkmsg(data, stepinfo)
    front_respone['msg'] = 'success'
    return JsonResponse(front_respone)


def dingrecord(request):
    ## 此接口是用于发布记录模块 钉 功能
    if request.method == 'POST' or request.method == 'post':
        res = json.loads(request.body.decode('utf-8'))


# alarm模块用于告知至dingding webhook
def dingtalkmsg(data, type):
    """
    :param data:
    :param type: 0 - 是未处理 1 - 失败 2 - 成功
    :return:
    https://moppowar.oss-ap-southeast-1.aliyuncs.com/midplatform/deploystatus/aduitok.png
    """
    deploystatus = {
        1: ["测试未通过", 'https://moppowar.oss-accelerate.aliyuncs.com/midplatform/deploystatus/testfail.png'],
        2: ["测试通过", 'https://moppowar.oss-accelerate.aliyuncs.com/midplatform/deploystatus/testok.png'],
        3: ["审核失败", 'https://moppowar.oss-accelerate.aliyuncs.com/midplatform/deploystatus/aduitfail.png'],
        4: ["审核通过", 'https://moppowar.oss-accelerate.aliyuncs.com/midplatform/deploystatus/aduitok.png'],
        5: ["部署失败", 'https://moppowar.oss-accelerate.aliyuncs.com/midplatform/deploystatus/arrangefail.png'],
        6: ["部署成功", 'https://moppowar.oss-accelerate.aliyuncs.com/midplatform/deploystatus/arrangeok.png'],
        7: ["发布失败", 'https://moppowar.oss-accelerate.aliyuncs.com/midplatform/deploystatus/deployfail.png'],
        8: ["发布成功", 'https://moppowar.oss-accelerate.aliyuncs.com/midplatform/deploystatus/deployok.png']
    }
    from project import models
    from common import baseconfig
    ossurl = baseconfig.getconfig()['baseFileUrl']
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    logo = ossurl + models.projectName.objects.values('projectLogo').filter(projectName=data['projectName']).first()['projectLogo']
    # projecthook = models.projectName.objects.values('projectHook').filter(projectName=data['projectName']).first()['projectHook']
    projecthook = '75e709c1a28e4d79d3ab6643ef5923d9409af252ca6cd3ed52dc4da40b1e98fc'
    api_url = "https://oapi.dingtalk.com/robot/send?access_token=" + projecthook

    ####获取该项目的项目经理用户ID
    from project import models as proownermol
    idList = proownermol.projectName.objects.filter(projectName=data['projectName']).values('projectOwnerId','opsOwnerId').first()

    from sysconf import models as  sysmol
    testnum = sysmol.sys_user.objects.filter(nickname=data['tester']).values('phone').first()['phone']
    ownerNum = sysmol.sys_user.objects.filter(id=int(idList['projectOwnerId'])).values('phone').first()['phone']
    opsNum = sysmol.sys_user.objects.filter(id=int(idList['opsOwnerId'])).values('phone').first()['phone']

    if type == 0:
        newdata = {
            "msgtype": "markdown",
            "markdown": {
                "title": "项目发布",
                "text": "### " + data['projectName'] + "更新概要\n" +
                        "> #### 更新模块：\r\n" + data['modifyModel'] + "\n\r" +
                        "> #### 更新内容：\r\n " + data['modifyContent'] + "\n\r" +
                        "> #### 开发人员： \r\n" + data['publisher'] + "\n\r" +
                        "> #### 测试人员： \r\n"  + "@" + testnum + "\n\r" +
                        "![screenshot](" + logo + ")\n"
            },
            "at": {
                "atMobiles": [
                    testnum
                ],
                "isAtAll": False
            }
        }
        data = newdata
    else:

        editdata = {
            "msgtype": "markdown",
            "markdown": {
                "title": "项目发布",
                "text": "### " + data['projectName'] + "***" + deploystatus[int(type)][0] + "***" + "\n" +
                        "![screenshot](" + deploystatus[int(type)][1] + ")\n" +
                        "> #### 更新模块：\r\n" + data['modifyModel'] + "\n\r" +
                        "> #### 更新内容：\r\n " + data['modifyContent'] + "\n\r" +
                        "> #### 开发人员： \r\n" + data['publisher'] + "\n\r" +
                        "> #### 测试人员： \r\n" + data['tester'] + "@" + testnum + "\n\r" +
                        "![screenshot](" + logo + ")\n"
            },
            "at": {
                "atMobiles": [
                    testnum
                ],
                "isAtAll": False
            }
        }
        data = editdata

    # requests.post(url=api_url, data=json.dumps(data), headers=headers)


##计算发布时长函数
def proTime(res):
    start_time = models.deployRecord.objects.values('deployTime').filter(pk=res['id']).first()['deployTime']
    ###数据库获取的值转换格式
    start_time = start_time.timestamp()
    stop_time = datetime.datetime.now().timestamp()
    firetime = (stop_time - start_time) / 60

    return int(firetime)

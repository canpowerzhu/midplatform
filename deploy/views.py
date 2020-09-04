from django.shortcuts import render, HttpResponse, HttpResponseRedirect
import json
import requests
from deploy import models
from django.conf import settings
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.db.models import Max
import datetime


##发布记录包含四个接口： addrecord、editrecord、getallrecord
#
#
def getallrecord(request):
    kwargs = {
        # 动态查询的字段
    }
    id = request.GET.get('id')
    if id:
        kwargs['id'] = int(id)
    limit = int(request.GET.get('limit', default=10))
    page = int(request.GET.get('page', default=1))

    projectName = request.GET.get('projectName')
    publisher = request.GET.get('publisher')
    state = request.GET.get('state')

    if publisher != None and projectName != None:
        kwargs['publisher'] = publisher
        kwargs['projectName'] = projectName

    elif projectName != None:
        kwargs['projectName'] = projectName

    elif state != None:
        kwargs['state'] = state

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

        if res['remark'] != None:
            kwargs['remark'] = res['remark']

        kwargs['projectName'] = res['projectName']
        kwargs['isRollBack'] = res['isRollBack']
        kwargs['modifyModel'] = res['modifyModel']
        kwargs['modifyContent'] = res['modifyContent']

        kwargs['tester'] = testname
        kwargs['state'] = 0
        kwargs['publisher'] = res['publisher']

        models.deployRecord.objects.create(**kwargs)
        get_res= models.deployRecord.objects.all().aggregate(Max('id'))

        front_respone = {'code': 2001, 'msg': None}
        front_respone['msg'] = 'success'
        res['tester'] = testname
        res['id'] = get_res['id__max']
        dingtalkmsg(res, 0)
        return JsonResponse(front_respone)


def editrecord(request):
    # del settings.RESULT['data']
    # del settings.RESULT['count']
    # 这里进行修改step状态
    kwargs = {

    }
    res = json.loads(request.body.decode('utf-8'))
    stepinfo = int(res['status'])
    finishTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    # 测试步骤

    curstep = models.deployRecord.objects.filter(pk=res['id']).values('step').first()['step']
    print(curstep, res['step'])
    if res['step'] < int(curstep):
        settings.RESULT['code'] = 20091
        settings.RESULT['msg'] = 'fail'
        settings.RESULT['date'] = '重复提交'
        return JsonResponse(settings.RESULT)
    else:
        kwargs['step'] = int(res['step']) + 1
    if stepinfo == 1 or stepinfo == 2:
        kwargs['state'] = 1
        kwargs['testStatus'] = res['status']
        kwargs['testResult'] = res['result']

    # 审核步骤
    if stepinfo == 3 or stepinfo == 4:
        kwargs['state'] = 1
        kwargs['aduitStatus'] = res['status']
        kwargs['aduitResult'] = res['result']

    # 部署步骤
    if stepinfo == 5 or stepinfo == 6:
        kwargs['state'] = 1
        kwargs['arrangeStatus'] = res['status']
        kwargs['arrangeResult'] = res['result']

    # 发布步骤
    if stepinfo == 7 or stepinfo == 8:
        kwargs['state'] = 1
        kwargs['deployStatus'] = res['status']
        kwargs['deployResult'] = res['result']
        kwargs['state'] = 3

    if stepinfo == 1 or stepinfo == 3 or stepinfo == 5 or stepinfo == 7:
        kwargs['state'] = 2
        kwargs['finishTime'] = finishTime
        kwargs['elapsedTime'] = proTime(res)
        settings.RESULT['code'] = 2009
        settings.RESULT['msg'] = 'fail'
    else:
        kwargs['finishTime'] = finishTime
        kwargs['elapsedTime'] = proTime(res)
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'

    models.deployRecord.objects.filter(pk=res['id']).update(**kwargs)
    data = model_to_dict(models.deployRecord.objects.get(pk=res['id']))
    dingtalkmsg(data, stepinfo)
    return JsonResponse(settings.RESULT)


def dingrecord(request):
    # 此接口是用于发布记录模块 钉 功能
    # 需要传参 针对哪个发布记录钉  钉哪一步
    if request.method == 'POST' or request.method == 'post':
        res = json.loads(request.body.decode('utf-8'))
        dingstep = int(res['dingStep'])  # dingstep  1 测试 2 审核 3 运维
        id = int(res['id'])
        dingcontent = models.deployRecord.objects.filter(pk=id).values('projectName', 'tester').first()
        data = {'id':id,'tester': dingcontent['tester'], 'dingstep': dingstep, 'projectName': dingcontent['projectName']}
        dingtalkmsg(data, 9)
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        return JsonResponse(settings.RESULT)


# alarm模块用于告知至dingding webhook
def dingtalkmsg(data, type):
    """
    :param data:
    :param type: 0 - 是未处理 1 - 失败 2 - 成功
    :return:
    https://moppowar.oss-ap-southeast-1.aliyuncs.com/midplatform/deploystatus/aduitok.png
    """
    from project import models
    from common import baseconfig
    ossurl = baseconfig.getconfig()['baseFileUrl']
    print(data)
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    logo = ossurl + models.projectName.objects.values('projectLogo').filter(projectName=data['projectName']).first()[
        'projectLogo']
    # projecthook = models.projectName.objects.values('projectHook').filter(projectName=data['projectName']).first()['projectHook']
    projecthook = '75e709c1a28e4d79d3ab6643ef5923d9409af252ca6cd3ed52dc4da40b1e98fc'
    api_url = "https://oapi.dingtalk.com/robot/send?access_token=" + projecthook

    # 获取该项目的项目经理用户ID
    from project import models as proownermol
    idList = proownermol.projectName.objects.filter(projectName=data['projectName']).values('projectOwnerId',
                                                                                            'opsOwnerId').first()

    from sysconf import models as  sysmol
    dowithbaseurl = baseconfig.getconfig()['dowithurl']
    print(data)
    url = dowithbaseurl + '?id='+ str(data['id'])
    # print(url)
    testnum = sysmol.sys_user.objects.filter(nickname=data['tester']).values('phone').first()['phone']
    ownerNum = sysmol.sys_user.objects.filter(id=int(idList['projectOwnerId'])).values('phone').first()['phone']
    opsNum = sysmol.sys_user.objects.filter(id=int(idList['opsOwnerId'])).values('phone').first()['phone']
    deploystatus = {
        0: ["发布开始，请前去补充测试结论", 'https://moppowar.oss-accelerate.aliyuncs.com/midplatform/deploystatus/newstart.png',
            testnum],
        1: ["测试未通过", 'https://moppowar.oss-accelerate.aliyuncs.com/midplatform/deploystatus/newtestfail.png'],
        2: ["测试通过，请前去审核", 'https://moppowar.oss-accelerate.aliyuncs.com/midplatform/deploystatus/newtestok.png',
            ownerNum],
        3: ["审核失败", 'https://moppowar.oss-accelerate.aliyuncs.com/midplatform/deploystatus/newaduitfail.png'],
        4: ["审核通过,请前去发布", 'https://moppowar.oss-accelerate.aliyuncs.com/midplatform/deploystatus/newaduitok.png',
            opsNum],
        5: ["部署失败", 'https://moppowar.oss-accelerate.aliyuncs.com/midplatform/deploystatus/newarrangefail.png'],
        6: ["部署成功，请进行线上测试", 'https://moppowar.oss-accelerate.aliyuncs.com/midplatform/deploystatus/newarrangeok.png',
            testnum],
        7: ["发布失败", 'https://moppowar.oss-accelerate.aliyuncs.com/midplatform/deploystatus/newdeployfail.png'],
        8: ["发布成功,线上测试正常", 'https://moppowar.oss-accelerate.aliyuncs.com/midplatform/deploystatus/newdeployok.png'],
        9: ["你有待处理的记录，请尽快处理", testnum, ownerNum, opsNum,
            'https://moppowar.oss-accelerate.aliyuncs.com/midplatform/deploystatus/newmsgalarm.png']
    }

    if type == 0 or type == 2 or type == 4 or type == 6:
        # 这是开发人员填写完成 @测试人员 数据
        if type == 0:
            data['testResult'] = '测试结论未填写'
        senddata = {
            "msgtype": "markdown",
            "markdown": {
                "title": "项目发布",
                "text": "### " + data['projectName'] + "***" + deploystatus[int(type)][0] + "***" + "\n" +
                        "![screenshot](" + logo + ")\n" +
                        "> #### 更新模块：\r\n" + data['modifyModel'] + "\n\r" +
                        "> #### 更新内容：\r\n " + data['modifyContent'] + "\n\r" +
                        "> #### 开发人员： \r\n" + data['publisher'] + "\n\r" +
                        "> #### 测试人员： \r\n" + data['tester'] + "\n\r" +
                        "@" + deploystatus[int(type)][2] + "\n\r" +
                        "![screenshot](" + deploystatus[int(type)][1] + ")\n\r" +
                        "  [去处理](" + url + ")" + "\n"

            },
            "at": {
                "atMobiles": [
                    deploystatus[int(type)][2]
                ],
                "isAtAll": False
            }
        }

    elif type == 1 or type == 3 or type == 5 or type == 7 or type == 8:
        # 这是任何一个阶段 失败的数据格式，默认@全体
        # 此外包含最后一步线上测试成功 数据格式 也是@全体
        senddata = {
            "msgtype": "markdown",
            "markdown": {
                "title": "项目发布",
                "text": "### " + data['projectName'] + "***" + deploystatus[int(type)][0] + "***" + "\n" +
                        "![screenshot](" + logo + ")\n" +
                        "> #### 更新模块：\r\n" + data['modifyModel'] + "\n\r" +
                        "> #### 更新内容：\r\n " + data['modifyContent'] + "\n\r" +
                        "> #### 开发人员： \r\n" + data['publisher'] + "\n\r" +
                        "> #### 测试人员： \r\n" + data['tester'] + "\n\r" +
                        "![screenshot](" + deploystatus[int(type)][1] + ")\n\r" +
                        "  [去处理](" + url + ")" + "\n"
            },
            "at": {
                "isAtAll": True
            }
        }

    else:
        # type = 9 是 钉功能

        senddata = {
            "msgtype": "markdown",
            "markdown": {
                "title": "项目发布",
                "text": "### 项目" + data['projectName'] + "\n" +
                        "### @" + deploystatus[int(type)][data['dingstep']] + "\n" +
                        "![screenshot](" + deploystatus[int(type)][4] + ")\n\r" +
                        "  [去处理](" + url + ")" + "\n"
            },
            "at": {
                "atMobiles": [
                    deploystatus[int(type)][data['dingstep']]
                ],
                "isAtAll": False
            }
        }
    requests.post(url=api_url, data=json.dumps(senddata), headers=headers)


##计算发布时长函数
def proTime(res):
    start_time = models.deployRecord.objects.values('deployTime').filter(pk=res['id']).first()['deployTime']
    ###数据库获取的值转换格式
    start_time = start_time.timestamp()
    stop_time = datetime.datetime.now().timestamp()
    firetime = (stop_time - start_time) / 60

    return int(firetime)


def issuerecord(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    if request.method == 'PUT' or request.method == 'put':
        res = json.loads(request.body.decode('utf-8'))
        kwargs = {'recordId': res['recordId'], 'title': res['title'], 'content': res['content'], 'srcIP': ip,
                  'username': res['userName']}
        try:
            models.issueRecord.objects.filter(id=res['id']).update(**kwargs)
            settings.RESULT['code'] = 2001
            settings.RESULT['msg'] = 'success'
        except Exception as e:
            settings.RESULT['code'] = 2002
            settings.RESULT['msg'] = 'fail'
            settings.RESULT['data'] = str(e)
        return JsonResponse(settings.RESULT)

    if request.method == 'POST' or request.method == 'post':
        res = json.loads(request.body.decode('utf-8'))
        kwargs = {'recordId': res['recordId'], 'title': res['title'], 'content': res['content'], 'srcIP': ip,
                  'username': res['userName']}
        try:
            models.issueRecord.objects.create(**kwargs)
            settings.RESULT['code'] = 2001
            settings.RESULT['msg'] = 'success'
        except Exception as e:
            settings.RESULT['code'] = 2002
            settings.RESULT['msg'] = 'fail'
            settings.RESULT['data'] = str(e)
        return JsonResponse(settings.RESULT)

    if request.method == 'GET' or request.method == 'get':
        # 这里有列表详情，和文章详情 依据是否有id判断
        # recordId = request.GET.get('recordId')
        # if recordId != None:
        #     data=models.issueRecord.objects.filter(pk=recordId).values().first()
        #     print(data)
        #     settings.RESULT['data'] = data
        #     settings.RESULT['code'] =2001
        #     settings.RESULT['msg'] = 'success'
        #     return JsonResponse(settings.RESULT)
        id = request.GET.get('recordId')
        if id == None:
            # 查询列表
            data = models.issueRecord.objects.all().values()
            settings.RESULT['data'] = list(data)
            settings.RESULT['count'] = data.count()
        else:
            # 查询详情
            print('ee')
            data = models.issueRecord.objects.filter(recordId=id).values()
            settings.RESULT['data'] = list(data)
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        return JsonResponse(settings.RESULT)


def issuerecordpic(request):
    res = json.loads(request.body.decode('utf-8'))
    from common import ossupload
    picurl = ossupload.uploadBase64Pic(res['img'], '', res['userName'])
    settings.RESULT['code'] = 2001
    settings.RESULT['msg'] = 'success'
    settings.RESULT['data'] = picurl
    del settings.RESULT['count']
    return JsonResponse(settings.RESULT)

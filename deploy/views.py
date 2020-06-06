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

    # if page == 1:
    #     start = 0
    #     stop = limit
    # else:
    #     start = (page - 1) * limit
    #     stop = limit * page

    projectName = request.GET.get('projectName')
    publisher = request.GET.get('publisher')

    kwargs = {
    # 动态查询的字段
    }
    if publisher != None and projectName != None:
        kwargs['publisher'] = publisher
        kwargs['projectName'] = projectName

    elif projectName != None:
        kwargs['ProjectName'] = projectName

    elif publisher != None :
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
        # print(datalist)
    else:
        # del settings.RESULT['count']
        # del settings.RESULT['data']
        settings.RESULT['code'] = 2002
        settings.RESULT['msg'] = "fail"
    return JsonResponse(settings.RESULT)


def addrecord(request):
    if request.method == 'POST':
        res = json.loads(request.body.decode('utf-8'))
        print(res)
        #TODO 没有缓存上传为0 需要判断
        #{'isModifyCache': 0, 'isModifySql': 0, 'projectName': '21212121', 'state': 0, 'isRollBack': 1, 'publisher': 'dixiaoping', 'modifyContent': '11212211221', 'modifyModel': '21233232122112'}
        kwargs ={
            ##动态参数
        }
        if res['isModifyCache'] == 1:
            kwargs['isModifyCache'] = 1
            kwargs['cacheDetail'] = res['cacheDetail']

        if res['isModifySql'] == 1:
            kwargs['isModifySql'] = 1
            kwargs['sqlDetail'] = res['sqlDetail']

        kwargs['projectName'] =res['projectName']
        kwargs['isRollBack'] =res['isRollBack']
        kwargs['modifyModel'] =res['modifyModel']
        kwargs['modifyContent'] =res['modifyContent']
        kwargs['state'] = 0
        kwargs['publisher'] =res['publisher']


        models.deployRecord.objects.create(**kwargs)
        front_respone = {'code': 2001, 'msg': None}
        front_respone['msg'] = 'success'
        # dingtalkmsg(res, 0)
        return JsonResponse(front_respone)


def editrecord(request):
    front_respone = {'code': 2001, 'msg': None}
    if request.method == 'POST':
        res = json.loads(request.body.decode('utf-8'))
    finishTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    models.deployRecord.objects.filter(pk=res['id']).update(state=res['state'], finishTime=finishTime,
                                                            elapsedTime=proTime(res))
    data = model_to_dict(models.deployRecord.objects.get(pk=res['id']))
    dingtalkmsg(data, int(res['state']))
    front_respone['msg'] = 'success'
    return JsonResponse(front_respone)


# alarm模块用于告知至dingding webhook
def dingtalkmsg(data, type):
    """
    :param data:
    :param type: 0 - 是未处理 1 - 失败 2 - 成功
    :return:
    """
    from project import models
    # from project.models import ProjectName
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    print(data)
    logo = models.projectName.objects.values('projectLogo').filter(projectName=data['projectName']).first()['projectLogo']
    projecthook = models.projectName.objects.values('projectHook').filter(projectName=data['projectName']).first()['projectHook']
    api_url = "https://oapi.dingtalk.com/robot/send?access_token=" + projecthook
    print(logo)
    if type == 0:
        newdata = {
            "msgtype": "markdown",
            "markdown": {
                "title": "项目发布",
                "text": "### " + data['projectName'] + "更新概要\n" +
                        "> #### 更新模块：\r\n" + data['modifyModel'] + "\n\r" +
                        "> #### 更新内容：\r\n " + data['modifyContent'] + "\n\r" +
                        "> #### 更新人员： \r\n" + data['publisher'] + "\n\r" +
                        "![screenshot](" + logo + ")\n"
            },
            "at": {
                "isAtAll": True
            }
        }
        data = newdata
    elif type == 2:
        editdata = {
            "msgtype": "markdown",
            "markdown": {
                "title": "项目发布",
                "text": "### " + data[
                    'projectName'] + "更新成功 \n" +
                        "![screenshot](https://moppowar.oss-accelerate.aliyuncs.com/projectlogo/ook.jpg)\n" +
                        "> #### 更新模块：\r\n" + data['modifyModel'] + "\n\r" +
                        "> #### 更新内容：\r\n " + data['modifyContent'] + "\n\r" +
                        "> #### 更新人员： \r\n" + data['publisher'] + "\n\r" +
                        "![screenshot](" + logo + ")\n"
            },
            "at": {
                "isAtAll": False
            }
        }
        data = editdata
    elif type == 1:
        editdata = {
            "msgtype": "markdown",
            "markdown": {
                "title": "项目发布",
                "text": "### " + data[
                    'projectName'] + "更新失败 \n" +
                        "![screenshot](https://moppowar.oss-accelerate.aliyuncs.com/projectlogo/fail.jpg)\n" +
                        "> #### 更新模块：\r\n" + data['modifyModel'] + "\n\r" +
                        "> #### 更新内容：\r\n " + data['modifyContent'] + "\n\r" +
                        "> #### 更新人员： \r\n" + data['publisher'] + "\n\r" +
                        "![screenshot](" + logo + ")\n"
            },
            "at": {
                "isAtAll": False
            }
        }
        data = editdata
    else:
        pass

    requests.post(url=api_url, data=json.dumps(data), headers=headers)


##计算发布时长函数
def proTime(res):
    start_time = models.deployRecord.objects.values('deployTime').filter(pk=res['id']).first()['deployTime']
    ###数据库获取的值转换格式
    start_time = start_time.timestamp()
    stop_time = datetime.datetime.now().timestamp()
    firetime = (stop_time - start_time) / 60

    return int(firetime)



# ## celery 定时任务
# from . import tasks
# def add(request,*args,**kwargs):
#   res = tasks.add.delay(1,2)
#   result = {'code': 0, 'msg': '这是一个后台任务'}
#   print(res)
#   return JsonResponse({'code':'successful','task_id':res.task_id})
#   # result = {'code': 0, 'msg': '这是一个后台任务'}
#   # return JsonResponse(result)
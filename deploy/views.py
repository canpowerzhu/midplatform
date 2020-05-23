from django.shortcuts import render, HttpResponse, HttpResponseRedirect
import json
import requests
from deploy import models
from django.conf import settings
from django.http import JsonResponse
from django.forms.models import model_to_dict


import datetime





##发布记录包含四个接口： addrecord、editrecord、getallrecord
#
#
def getallrecord(request):
    limit = int(request.GET.get('limit', default='10'))
    page = int(request.GET.get('page', default='1'))

    if page == 1:
        start = 0
        stop = limit
    else:
        start = (page - 1) * limit
        stop = limit * page

    ProjectName = request.GET.get('ProjectName')
    Publisher = request.GET.get('Publisher')

    if Publisher != None and ProjectName != None:
        count = models.DeployRecord.objects.filter(ProjectName=ProjectName, Publisher=Publisher).count()
        res = models.DeployRecord.objects.filter(ProjectName=ProjectName, Publisher=Publisher).order_by('-DeployTime')

    if ProjectName != None:
        count = models.DeployRecord.objects.filter(ProjectName=ProjectName).count()
        res = models.DeployRecord.objects.filter(ProjectName=ProjectName).order_by('-DeployTime').values()

    if Publisher != None :
        count = models.DeployRecord.objects.filter(Publisher=Publisher).count()
        res = models.DeployRecord.objects.filter(Publisher=Publisher).order_by('-DeployTime')

    datalist = list(res)
    if len(res) > 0:
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        settings.RESULT['count'] = count
        settings.RESULT['data'] = datalist
    else:
        del settings.RESULT['count']
        del settings.RESULT['data']
        settings.RESULT['code'] = 2002
        settings.RESULT['msg'] = "fail"
    return JsonResponse(settings.RESULT)


def addrecord(request):
    if request.method == 'POST':
        res = json.loads(request.body.decode('utf-8'))
        # 这里转换前端传来的开关状态值 为0 or 1
        transferlist = ['isModifyCache', 'isModifySql', 'isRollBack', 'state']
        for i in transferlist:
            if i in res:
                res[i] = 1
            else:
                res[i] = 0
        models.DeployRecord.objects.create(ProjectName=res['ProjectName'],
                                           isRollBack=res['isRollBack'],
                                           ModifyModel=res['ModifyModel'],
                                           ModifyContent=res['ModifyContent'],
                                           ###新增的记录状态均为未处理
                                           state=0,
                                           Publisher=res['Publisher'],
                                           isModifyCache=res['isModifyCache'],
                                           CacheDetail=res['CacheDetail'],
                                           isModifySql=res['isModifySql'],
                                           SqlDetail=res['SqlDetail'])
        front_respone = {'code': 2001, 'msg': None}

        front_respone['msg'] = 'success'
        # dingtalkmsg(res, 0,0)
        return JsonResponse(front_respone)


def editrecord(request):
    front_respone = {'code': 2001, 'msg': None}
    if request.method == 'POST':
        res = json.loads(request.body.decode('utf-8'))
    FinishTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    models.DeployRecord.objects.filter(pk=res['id']).update(state=res['state'], FinishTime=FinishTime,
                                                            ElapsedTime=proTime(res))
    data = model_to_dict(models.DeployRecord.objects.get(pk=res['id']))

    # dingtalkmsg(data, res['state'])
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
    logo = models.ProjectName.objects.values('ProjectLogo').filter(projectName=data['ProjectName']).first()[
        'ProjectLogo']
    projecthook = models.ProjectName.objects.values('ProjectHook').filter(projectName=data['ProjectName']).first()[
        'ProjectHook']
    api_url = "https://oapi.dingtalk.com/robot/send?access_token=" + projecthook
    print(api_url)
    if type == 0:
        newdata = {
            "msgtype": "markdown",
            "markdown": {
                "title": "项目发布",
                "text": "### " + data['ProjectName'] + "更新概要\n" +
                        "> #### 更新模块：\r\n" + data['ModifyModel'] + "\n\r" +
                        "> #### 更新内容：\r\n " + data['ModifyContent'] + "\n\r" +
                        "> #### 更新人员： \r\n" + data['Publisher'] + "\n\r" +
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
                    'ProjectName'] + "更新成功 \n" +
                        "![screenshot](https://moppowar.oss-accelerate.aliyuncs.com/projectlogo/ook.jpg)\n" +
                        "> #### 更新模块：\r\n" + data['ModifyModel'] + "\n\r" +
                        "> #### 更新内容：\r\n " + data['ModifyContent'] + "\n\r" +
                        "> #### 更新人员： \r\n" + data['Publisher'] + "\n\r" +
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
                    'ProjectName'] + "更新失败 \n" +
                        "![screenshot](https://moppowar.oss-accelerate.aliyuncs.com/projectlogo/fail.jpg)\n" +
                        "> #### 更新模块：\r\n" + data['ModifyModel'] + "\n\r" +
                        "> #### 更新内容：\r\n " + data['ModifyContent'] + "\n\r" +
                        "> #### 更新人员： \r\n" + data['Publisher'] + "\n\r" +
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
    start_time = models.DeployRecord.objects.values('DeployTime').filter(pk=res['id']).first()['DeployTime']
    ###数据库获取的值转换格式
    start_time = start_time.timestamp()
    stop_time = datetime.datetime.now().timestamp()
    firetime = (stop_time - start_time) / 60

    return int(firetime)



## celery 定时任务
from . import tasks
def add(request,*args,**kwargs):
  res = tasks.add.delay(1,2)
  result = {'code': 0, 'msg': '这是一个后台任务'}
  print(res)
  return JsonResponse({'code':'successful','task_id':res.task_id})
  # result = {'code': 0, 'msg': '这是一个后台任务'}
  # return JsonResponse(result)
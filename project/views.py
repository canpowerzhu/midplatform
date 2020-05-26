from django.shortcuts import HttpResponse
from django.http import JsonResponse
from project import models
import json
from midplatform import settings
import datetime
from project.models import projectName
from common import unpack

from django.views.decorators.csrf import csrf_exempt


# Create your views here.

##项目管理
# 项目基础信息包含四个接口： getbaseinfo、modifybaseinfo、addbaseinfo
def getbaseinfo(request):
    limit = int(request.GET.get('limit', default='10'))
    page = int(request.GET.get('page', default='1'))
    ProjectName = request.GET.get('ProjectName', default=None)


    if page == 1:
        start = 0
        stop = limit
    else:
        start = (page - 1) * limit
        stop = limit * page
    if  ProjectName != None:
        res = models.projectName.objects.filter(projectName=projectName)
    else:
        res = models.projectName.objects.all().order_by('-id')[start:stop]
    count = models.projectName.objects.count()
    if len(res) > 0:
        datalist = []
        for i in range(len(res)):
            initData = {"id": None, "projectName": None, "projectHook": None, "projectModel": None, "projectLogo": None,
                        "status": None, "updateTime": None}
            initData['id'] = res[i].id
            initData['projectName'] = res[i].projectName
            initData['projectHook'] = res[i].projectHook
            initData['projectModel'] = res[i].projectModel
            initData['projectLogo'] = res[i].projectLogo
            initData['status'] = res[i].status
            initData['updateTime'] = res[i].updateTime.strftime('%Y-%m-%d %H:%M:%S')
            datalist.append(initData)
        # print(datalist)
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        settings.RESULT['count'] = count
        settings.RESULT['data'] = datalist
        data = json.dumps(settings.RESULT)
        return HttpResponse(data)
    else:
        settings.RESULT['msg'] = "fail"
        print(settings.RESULT)
    return HttpResponse("fail")


def modifybaseinfo(request):
    """
    :func 修改对应的数据条目
    :param request:
    :return:
    """
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        front_respone = {'code': 2001, 'msg': None}
        try:
            models.projectName.objects.filter(pk=data['id']).update(projectName=data['projectName'],
                                                                    projectModel=data['projectModel'],
                                                                    status=data['status'],
                                                                    updateTime=datetime.datetime.now(),
                                                                    projectLogo=data['projectLogo'])
        except Exception as e:

            front_respone['msg'] = 'fail'
        else:
            front_respone['msg'] = 'success'
        return JsonResponse(front_respone)



def addbaseinfo(request):
    """
    : func 新增项目
    :param request:
    :return:
    """
    if request.method == 'POST':
        res = json.loads(request.body.decode('utf-8'))
        # if res['status'] == 'on':
        #     statusinfo = 1
        # else:
        #     statusinfo = 0
        front_respone = {'code': None, 'msg': None}
        try:
            models.projectName.objects.create(projectName=res['projectName'],
                                              projectModel=res['projectModel'],
                                              status=res['status'],
                                              projectHook=res['projectHook'],
                                              projectLogo=res['projectLogo'])
        except Exception as e:
            print(e)
            front_respone['code'] = '2002'
            front_respone['msg'] = 'fail'
        else:
            front_respone['code'] = '2001'
            front_respone['msg'] = 'success'
        return JsonResponse(front_respone)


def addprojectlogo(request):
    # TODO 新增项目增加一个logo图片上传接口
    pass


def getproname(request):
    final_data = {"code": 2001, "msg": "success", "data": None}
    res = models.projectName.objects.values('projectName').all()
    if len(res) > 0:
        data = {}
        for i in range(len(res)):
            data[res[i]['projectName']] = res[i]['projectName']
        final_data['data'] = data
        return JsonResponse(final_data)


def getmodelname(request):
    final_data = {"code": 2001, "msg": "success", "data": None}
    proname = request.GET.get('proname')
    data = {}
    res = models.projectName.objects.values('projectModel').filter(projectName=proname).first()['projectModel'].split(
        ',')
    for i in res:
        data[i] = i
    final_data['data'] = data
    return JsonResponse(final_data)


###项目login相关view
def urlinfo(request):
    limit = int(request.GET.get('limit', default='10'))
    page = int(request.GET.get('page', default='1'))
    project = request.GET.get('project', default=None)
    # TODO 这里的project_type 不要使用汉字描述，采取其他标记 可以设计一个表
    project_type = request.GET.get('project_type', default=None)

    if page == 1:
        start = 0
        stop = limit
    else:
        start = (page - 1) * limit
        stop = limit * page

    kwargs = {}
    if project_type != None:
        kwargs['project_type'] = project_type

    if project != None:
        kwargs['project'] = project

    if project != None and project_type != None:
        kwargs['project'] = project
        kwargs['project_type'] = project_type

    res = models.projectinfo.objects.filter(**kwargs).order_by('-id')
    count = res.count()
    if project == None and project_type == None:
        count = models.projectinfo.objects.count()
        res = models.projectinfo.objects.all().order_by('-id')[start:stop]

    if len(res) > 0:
        datalist = []
        for i in range(len(res)):
            if res[i].gologin:
                status = 1
            else:
                status = 0
            initData = {"id": None, "project": None, "project_type": None, "website_url": None,
                        "gologin": None, "remarks": None}
            initData['id'] = res[i].id
            initData['project'] = res[i].project
            initData['project_type'] = res[i].project_type
            initData['website_url'] = res[i].website_url
            initData['gologin'] = status
            initData['remarks'] = res[i].remarks
            datalist.append(initData)

        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        settings.RESULT['count'] = count
        settings.RESULT['data'] = datalist

    else:
        settings.RESULT['msg'] = "fail"
        print(settings.RESULT)

    return JsonResponse(settings.RESULT)  # return HttpResponse(settings.RESULT)


def urlinfoselect(request):
    final_data = {"code": 2001, "data": None}
    data = {'project': [], 'project_type': []}
    project_res = models.projectinfo.objects.values('project').distinct()
    for item in project_res:
        data['project'].append(item['project'])

    project_type_res = models.projectinfo.objects.values('project_type').distinct()
    for item in project_type_res:
        data['project_type'].append(item['project_type'])
    final_data['data'] = data
    return JsonResponse(final_data)


def addurlinfo(request):
    if request.method == 'POST':
        res = json.loads(request.body.decode('utf-8'))
        front_respone = {'code': 2001, 'msg': None}
        models.projectinfo.objects.create(project=res['project'],
                                          project_type=res['project_type'],
                                          website_url=res['website_url'],
                                          gologin=res['gologin'])
        front_respone['msg'] = 'success'
        return JsonResponse(front_respone)


def editlogin(request):
    front_respone = {'code': 2001, 'msg': None}
    if request.method == 'POST':
        res = json.loads(request.body.decode('utf-8'))
        if res['gologin']:
            state = 1
        else:
            state = 0

        models.projectinfo.objects.filter(pk=res['id']).update(gologin=state)
        front_respone['msg'] = 'success'
        return JsonResponse(front_respone)

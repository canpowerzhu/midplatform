from django.shortcuts import render

# Create your views here.

from django.shortcuts import HttpResponse
from midplatform import settings
from django.http import JsonResponse
from component import models
from common import unpack
### 获取现有的apk上传列表
def getapklist(request):
    limit = int(request.GET.get('limit', default='10'))
    page = int(request.GET.get('page', default='1'))
    envtype = request.GET.get('envtype')
    if page == 1:
        start = 0
        stop = limit
    else:
        start = (page - 1) * limit
        stop = limit * page

    if envtype != '' or envtype != None:
        res = models.apklist.objects.filter(envtype=envtype)
        count = res.count()
    if envtype == None:
        count = models.apklist.objects.count()
        res = models.apklist.objects.all()[start:stop]

    if len(res) > 0:
        datalist = []
        for i in range(len(res)):
            if res[i].envtype:
                envtype = '正式'
            else:
                envtype = '测试'
            initData = {"id": None, "projectname": None, "packagename": None, "version": None,
                        "envtype": None, "size": None, "owner": None, "url": None, "createtime": None}
            initData['id'] = res[i].id
            initData['projectname'] = res[i].projectname
            initData['packagename'] = res[i].packagename
            initData['version'] = res[i].version
            initData['envtype'] = envtype
            initData['size'] = res[i].size
            initData['owner'] = res[i].owner
            initData['url'] = res[i].url
            initData['createtime'] = res[i].createtime.strftime('%Y-%m-%d %H:%M:%S')
            datalist.append(initData)
        settings.RESULT['code'] = 0
        settings.RESULT['msg'] = 'success'
        settings.RESULT['count'] = count
        settings.RESULT['data'] = datalist

    else:
        settings.RESULT['msg'] = "fail11"
        settings.RESULT['data'] = None

    return JsonResponse(settings.RESULT)
### 文件上传操作
# @csrf_exempt
def upload(request):
    if request.method == 'POST':
        owner = request.POST.get('owner')
        projectname = request.POST.get('projectname')
        envtype = request.POST.get('off_or_on')
        print(owner,projectname,envtype)
        if envtype:
            envtype = 'online'
        else:
            envtype = 'offline'
        file = request.FILES.get('file', None)
        print(file.size)
        size = round((int(file.size) / 1024 / 1024), 2)
        print(size)
        if file is None:
            return HttpResponse('没有需要上传的文件')
        else:
            from common import ossupload

            url = ossupload.update_fil_file(envtype, projectname, file.name, file)
            if envtype:
                envtype = 1
            else:
                envtype = 0

            ###解析apk文件 放在上传之后 否则上传的文件不可用
            apk = unpack.parse_apk(file)
             # 文件大小

            models.apklist.objects.create(projectname=projectname,
                                          packagename=apk.package_name,
                                          version=apk.version_code,
                                          envtype=envtype,
                                          size=size,
                                          owner=owner,
                                          url=str(url))
            finaldata = {'code': 0, 'msg': 'success'}
    return JsonResponse(finaldata)

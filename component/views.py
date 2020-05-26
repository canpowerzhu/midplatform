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
    envType = request.GET.get('envType')
    if page == 1:
        start = 0
        stop = limit
    else:
        start = (page - 1) * limit
        stop = limit * page

    if envType != None :
        res = models.apklist.objects.filter(envType=envType).values()
        count = res.count()
    else:
        count = models.apklist.objects.count()
        res = models.apklist.objects.all().values()[start:stop]

    if len(res) > 0:
        datalist = list(res)
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        settings.RESULT['count'] = count
        settings.RESULT['data'] = datalist
    else:
        settings.RESULT['code'] = 2002
        settings.RESULT['msg'] = "fail"

    return JsonResponse(settings.RESULT)
### 文件上传操作
# @csrf_exempt
def upload(request):
    if request.method == 'POST':
        owner = request.POST.get('owner')
        projectName = request.POST.get('projectname')
        envType = int(request.POST.get('envtype'))
        file = request.FILES.get('file', None)
        size = round((int(file.size) / 1024 / 1024), 2)
        if file is None:
            return HttpResponse('没有需要上传的文件')
        else:
            from common import ossupload

            url = ossupload.update_fil_file(envType, projectName, file.name, file)
            apk = unpack.parse_apk(file)
             # 文件大小

            models.apklist.objects.create(projectName=projectName,
                                          packageName=apk.package_name,
                                          version=apk.version_code,
                                          envType=int(envType),
                                          size=size,
                                          owner=owner,
                                          url=str(url))
            finaldata = {'code': 2001, 'msg': 'success'}
    return JsonResponse(finaldata)

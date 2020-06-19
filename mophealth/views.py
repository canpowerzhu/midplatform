from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from midplatform import  settings
from mophealth import models
import json
def tasklist(request):
    if request.method == 'GET' or request.method == 'get':
        res=models.taskList.objects.filter(deleted=1).values()
        settings.RESULT['count'] = res.count()
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        settings.RESULT['data'] = list(res)
        return JsonResponse(settings.RESULT)

    if request.method == 'POST' or request.method == 'post':
        res=json.loads(request.body.decode('utf-8'))
        models.taskList.objects.create(**res)
        settings.finalData['code']=2001
        settings.finalData['msg'] ='success'

        return JsonResponse(settings.finalData)
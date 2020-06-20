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


    elif request.method == 'POST' or request.method == 'post':
        res=json.loads(request.body.decode('utf-8'))
        models.taskList.objects.create(**res)
        settings.RESULT['code']=2001
        settings.RESULT['msg'] ='success'


    elif request.method == 'PUT' or request.method == 'put':
        res = json.loads(request.body.decode('utf-8'))
        print(res)
        # models.taskList.objects.filter(pk=res['id']).update(**res)
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'

    elif request.method == 'DELETE' or request.method == 'delete':
        res = int(request.GET.get('id'))
        models.taskList.objects.filter(pk=res['id']).update(deleted=0)
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'


    return JsonResponse(settings.RESULT)
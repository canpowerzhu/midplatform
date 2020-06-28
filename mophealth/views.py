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
        models.taskList.objects.filter(pk=res['id']).update(**res)
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'

    elif request.method == 'DELETE' or request.method == 'delete':
        res = int(request.GET.get('id'))
        models.taskList.objects.filter(pk=res['id']).update(deleted=0)
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'


    return JsonResponse(settings.RESULT)

def test(request):
    from midcelery.gettask.tasks import getUrl
    # 异步任务
    # send_sms.delay('119')
    # send_sms2.delay('110')

    # 定时任务
    import datetime
    from datetime import timedelta
    ##获取间隔时间
    delayTime = int(request.GET.get('intervalTime'))
    utc_ctime = datetime.datetime.utcfromtimestamp(datetime.datetime.now().timestamp())
    task_time = utc_ctime + timedelta(seconds=delayTime)
    url = 'http://bus.dominoppo.in/domino-webapi/rest/actuator/health'
    result = getUrl.apply_async([url,], eta=task_time)
    print(result)
    return JsonResponse({'code':'200','id':result.id})


def test2(request):
    from mophealth import midscheduler
    taskid = request.GET.get('taskid')
    opstype = int(request.GET.get('type',default=0))
    taskinfo = list(models.taskList.objects.filter(pk=int(taskid)).values_list('taskUrl','taskRate').first())
    print(len(taskinfo),taskinfo)
    taskUrl = taskinfo[0]
    taskRate = taskinfo[1]

    if taskid == None:
        return JsonResponse({'code':2001,'status':'fail','msg':'缺少taskid参数'})
    data = midscheduler.run(taskid,taskUrl,taskRate,opstype)
    settings.RESULT['code'] =2001
    settings.RESULT['data'] = str(data)
    print(json.dumps(settings.RESULT))
    return  HttpResponse(json.dumps(settings.RESULT))
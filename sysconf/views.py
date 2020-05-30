from django.http import HttpResponse, JsonResponse
from sysconf import models
from midplatform import settings
from django.forms.models import model_to_dict
from common import midplatformcrypt
import  json

from django.db.models import Q


##路由配置
def getrouter(request):
    if request.method == 'GET' or request.method == 'get':
        router = models.sys_menu.objects.all().filter(~Q(type=2)).values('component','hidden','icon','sort','id','KeepAlive','parentId','path','redirect','routerName','target','title','type','code')
        settings.RESULT['count'] = router.count()
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        settings.RESULT['data'] = list(router)
        return JsonResponse(settings.RESULT)

def router(request):
    if request.method == 'GET' or request.method == 'get':
        router = models.sys_menu.objects.all().values('component','hidden','icon','sort','id','KeepAlive','parentId','path','redirect','routerName','target','title','type','code')
        settings.RESULT['count'] = router.count()
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        settings.RESULT['data'] = list(router)


    elif request.method == 'DELETE' or request.method == 'delete':

        res = int(request.GET.get('id'))
        models.sys_menu.objects.filter(pk=res['id']).delete()
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        # return JsonResponse(settings.RESULT)

    elif request.method == 'PUT' or request.method == 'put':
        res = json.loads(request.body.decode('utf-8'))
        models.sys_menu.objects.filter(pk=res['id']).update(**res)
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        # return JsonResponse(settings.RESULT)

    elif request.method == 'POST' or request.method == 'post':
        router_dict = json.loads(request.body.decode('utf-8'))
        models.sys_menu.objects.create(**router_dict)
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
    return JsonResponse(settings.RESULT)


## oss配置相关两个接口
def ossconf(request):
    try:
        res = model_to_dict(models.ossconf.objects.all().first())
    except:
        finaldata = {'code': 2002, 'msg': 'fail', 'data': None}
        del finaldata['data']
        return JsonResponse(finaldata)
    else:
        # print(res['accessSecret'])
        cryptdata = Aescrypt(res['accessSecret'])
        res['accessSecret']= cryptdata['jiami']
        del res['id']
        finaldata = {'code': 2001, 'msg': 'success','data':None}
        finaldata['data'] = res
        return JsonResponse(finaldata)


def modifyossconf(request):
    if request.method == 'POST':
        import json
        res = json.loads(request.body.decode('utf-8'))
        print(res,type(res))
        count = models.ossconf.objects.all().count()
        if count == 0:
            models.ossconf.objects.create(**res)
        else:
            models.ossconf.objects.update(**res)

        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
    return JsonResponse(settings.RESULT)


## 邮件配置相关
def mailserver(request):
    pass


def changemailserver(request):
    if request.method == 'POST':
        res = request.body.decode('utf-8')
        print(res)

    return HttpResponse('success')


def Aescrypt(reqsecret):

    back_data = {}
    ###这里初始化加密对象 传入key 初始化密钥, 以及对应的偏移量
    text = midplatformcrypt.midowncrppt('i am wonderful!!', 'i am a offset wq')
    e = text.encrypt(reqsecret)
    jie_mi = text.decrypt(e)
    back_data['jiami'] = e.decode('utf-8')
    back_data['jiemi'] = jie_mi
    return back_data



def getuser(request):
    pass
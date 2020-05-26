from django.http import HttpResponse, JsonResponse
from sysconf import models
from midplatform import settings
from django.forms.models import model_to_dict
from common import midplatformcrypt
import  json


##路由配置

def addrouter(reuqest):
    if reuqest.method == 'POST':
        router_dict = json.loads(reuqest.body.decode('utf-8'))
        models.sys_menu.objects.create(**router_dict)
    # del settings.RESULT['count']
    # del settings.RESULT['data']
    settings.RESULT['code'] = 2001
    settings.RESULT['msg'] = 'success'
    return JsonResponse(settings.RESULT)

def editrouter(reuqest):
    if reuqest.method == 'POST':
        res = reuqest.body.decode('utf-8')
    return HttpResponse('ok')


def router(request):
    router = models.sys_menu.objects.all().values('component','hidden','icon','id','keep_alive','parentId','path','redirect','routerName','target','title')

    # print(list(router))
    settings.RESULT['count'] = router.count()
    settings.RESULT['code'] = 2001
    settings.RESULT['msg'] = 'success'
    settings.RESULT['data'] = list(router)
    return  JsonResponse(settings.RESULT)


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
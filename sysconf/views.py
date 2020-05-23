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
        print(router_dict, type(router_dict))
        # for k,v in res.items():
        #     print("字段是%s: 值是%s" %(k,v))
#TODO 注意这里可以采用字典打散方式存储与更新 注意修改对应代码
        models.sys_menu.objects.create(**router_dict)

    return HttpResponse('ok')
    # return  JsonResponse(respone)

def editrouter(reuqest):
    if reuqest.method == 'POST':
        res = reuqest.body.decode('utf-8')
        print(res)
    return HttpResponse('ok')
    # return  JsonResponse(respone)
def router(request):
    router = models.sys_menu.objects.all().values('component','hidden','icon','id','keep_alive','parent_id','path','redirect','router_name','target','title')
    print(list(router))
    del settings.RESULT['count']
    settings.RESULT['code'] = 2001
    settings.RESULT['msg'] = 'success'
    settings.RESULT['data'] = list(router)
    return  JsonResponse(settings.RESULT)

# def router(request):
#     top_menu = models.sys_menu.objects.filter(parent_id=0)
#     if len(top_menu) > 0:
#         data_list = []
#         for i in range(len(top_menu)):
#             sub_id = top_menu[i].menu_id
#             init_top_menu = {}
#             init_top_menu['name'] = top_menu[i].name
#             init_top_menu['title'] = top_menu[i].title
#             init_top_menu['icon'] = top_menu[i].icon
#             init_top_menu['list'] = subrouter(sub_id)
#             data_list.append(init_top_menu)
#
#         settings.RESULT['code'] = 0
#         settings.RESULT['msg'] = 'success'
#         settings.RESULT['data'] = data_list
#     return JsonResponse(settings.RESULT)
#
#
# def subrouter(sub_id):
#     second_menu = models.sys_menu.objects.filter(parent_id=sub_id)
#     data_list = []
#     for i in range(len(second_menu)):
#         init_data = {}
#         res = models.sys_menu.objects.filter(parent_id=second_menu[i].menu_id)
#         if len(res) == 0:
#             init_data['name'] = second_menu[i].name
#             init_data['title'] = second_menu[i].title
#             init_data['jump'] = second_menu[i].jump
#             data_list.append(init_data)
#         else:
#             res = subrouter(second_menu[i].menu_id)
#             half_init = {}
#             half_init['name'] = second_menu[i].name
#             half_init['title'] = second_menu[i].title
#             half_init['list'] = res
#             data_list.append(half_init)
#
#     return data_list


## oss配置相关两个接口
def ossconf(request):
    try:
        res = model_to_dict(models.ossconf.objects.get(pk=1))
    except:
        finaldata = {'code': 2002, 'msg': 'fail', 'data': None}
        del finaldata['data']
        return JsonResponse(finaldata)
    else:
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
        settings.RESULT['data'] = 'success'
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
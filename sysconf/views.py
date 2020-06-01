from django.http import HttpResponse, JsonResponse
from sysconf import models
from midplatform import settings
from django.forms.models import model_to_dict
from common import midplatformcrypt
import  json
from django.core.paginator import Paginator
from django.db.models import Q
from common import ossupload


##路由配置
def getrouter(request):
    """
    当前用户所拥有的权限菜单获取
    :param request:
    :return:
    """
    if request.method == 'GET' or request.method == 'get':
        router = models.sys_menu.objects.filter(deleted=0).filter(~Q(type=2)).values('component','hidden','icon','sort','id','KeepAlive','parentId','path','redirect','routerName','target','title','type','code')
        settings.RESULT['count'] = router.count()
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        settings.RESULT['data'] = list(router)
        return JsonResponse(settings.RESULT)

def router(request):
    """
    权限菜单管理 获取路由
    :param request:
    :return:
    """
    if request.method == 'GET' or request.method == 'get':
        router = models.sys_menu.objects.filter(deleted=0).values('component','hidden','icon','sort','id','KeepAlive','parentId','path','redirect','routerName','target','title','type','code')
        settings.RESULT['count'] = router.count()
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        settings.RESULT['data'] = list(router)


    elif request.method == 'DELETE' or request.method == 'delete':

        res = int(request.GET.get('id'))
        models.sys_menu.objects.filter(pk=res['id']).update(deleted=1)
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
    text = midplatformcrypt.midowncrppt('===bWlkcGxhdGZvcm0gYXV0aA=====', '==bWlkcGxhdGZvcm0gb2Zmc2V0==')
    e = text.encrypt(reqsecret)
    jie_mi = text.decrypt(e)
    back_data['jiami'] = e.decode('utf-8')
    back_data['jiemi'] = jie_mi
    return back_data



def sysuser(request):
    """
    权限菜单管理 获取路由
    :param request:
    :return:
    """
    if request.method == 'GET' or request.method == 'get':
        """
        type 传的是当前用户的用户类型，返回下级的所有用户 数字越小 级别越高
        """
        sysUserType = int(request.GET.get('type'))
        limit = int(request.GET.get('limit',default=10))
        page = int(request.GET.get('page', default=1))
        username = request.GET.get('username')
        nickname = request.GET.get('nickname')
        phone = request.GET.get('phone')
        kwargs ={
            ##动态查询条件
        }
        if username != None:
            kwargs['username'] = username
        if nickname != None:
            kwargs['nickname'] = nickname
        if phone != None:
            kwargs['phone'] = phone


        sysUser = models.sys_user.objects.filter(type__gte=sysUserType,deleted=0).filter(**kwargs).order_by('-createTime').values('id','username','nickname','password','salt','avatar','gender','email','phone','status','type','deleted','createTime','updateTime')
        paginator = Paginator(sysUser, limit)
        # 获取第2页的数据
        pageData = paginator.page(page)
        records = list(pageData)
        if len(records) == 0:
            settings.RESULT['code'] = 2002
            settings.RESULT['msg'] = 'fail'
        else:
            settings.RESULT['count'] = sysUser.count()
            settings.RESULT['code'] = 2001
            settings.RESULT['msg'] = 'success'
            settings.RESULT['data'] = records


    elif request.method == 'DELETE' or request.method == 'delete':

        res = int(request.GET.get('id'))
        models.sys_user.objects.filter(pk=res['id']).update(deleted=1)
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'


    elif request.method == 'PUT' or request.method == 'put':
        res = json.loads(request.body.decode('utf-8'))
        if 'avatar' in res.keys():
            if res['avatar'].split('/')[0] != 'midplatform':
                avatarPath=ossupload.uploadBase64Pic(res['avatar'])
                if avatarPath != None:
                    res['avatar'] =avatarPath
                else:
                    settings.RESULT['code'] = 2002
                    settings.RESULT['msg'] = 'fail'
                    return JsonResponse(settings.RESULT)
        models.sys_user.objects.filter(pk=res['id']).update(**res)
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'

    elif request.method == 'POST' or request.method == 'post':
        sysUserDict = json.loads(request.body.decode('utf-8'))
        if sysUserDict['avatar'] != None:
            avatarPath=ossupload.uploadBase64Pic(sysUserDict['avatar'])
            if avatarPath != None:
                sysUserDict['avatar'] =avatarPath
            else:
                settings.RESULT['code'] = 2002
                settings.RESULT['msg'] = 'fail'
                return JsonResponse(settings.RESULT)
        models.sys_user.objects.create(**sysUserDict)
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
    return JsonResponse(settings.RESULT)
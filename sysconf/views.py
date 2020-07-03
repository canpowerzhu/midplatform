from django.http import HttpResponse, JsonResponse
from sysconf import models
from midplatform import settings
from django.forms.models import model_to_dict
import json
from django.core.paginator import Paginator
from django.db.models import Q
from common import ossupload,midplatformcrypt,tokenserver

isLogin=tokenserver.isLogin

##路由配置
# @tokenserver.isLogin
def getrouter(request):
    """
    当前用户所拥有的权限菜单获取
    :param request:
    :return:
    """
    auth = request.META.get('HTTP_AUTHORIZATION')
    from common import tokenserver
    try:
        username = tokenserver.get_token(auth)['username']
    except Exception as e:
        settings.RESULT['code'] = 20032
        settings.RESULT['msg'] = str(e)
        return JsonResponse(settings.RESULT)
    user_id = models.sys_user.objects.filter(username=username).values('id').first()['id']
    roleid = models.sys_user_role.objects.filter(user_id=int(user_id)).values('role_id').first()['role_id']
    rolemenu = models.sys_role_menu.objects.filter(role_id=int(roleid)).values_list('permission_id',flat=True)
    rolemenuList = list(rolemenu)
    if request.method == 'GET' or request.method == 'get':
        router = models.sys_menu.objects.filter(id__in=rolemenuList).filter(deleted=1).filter(~Q(type=2)).values('component', 'hidden', 'icon',
                                                                                     'sort', 'id', 'KeepAlive',
                                                                                     'parentId', 'path', 'redirect',
                                                                                     'routerName', 'target', 'title',
                                                                                     'type', 'code')
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
    auth = request.META.get('HTTP_AUTHORIZATION')
    if request.method == 'GET' or request.method == 'get':
        router = models.sys_menu.objects.filter(deleted=1).values('component', 'hidden', 'icon', 'sort', 'id',
                                                                  'KeepAlive', 'parentId', 'path', 'redirect',
                                                                  'routerName', 'target', 'title', 'type', 'code')
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
    if request.method == 'GET' or request.method == 'get':
        try:
            res = model_to_dict(models.ossconf.objects.all().first())
        except:
            finaldata = {'code': 2002, 'msg': 'fail', 'data': None}
            del finaldata['data']
        else:
            finaldata = {'code': 2001, 'msg': 'success', 'data': None}
            finaldata['data'] = res
        return JsonResponse(finaldata)

    if request.method == 'POST' or request.method == 'post':
        import json
        res = json.loads(request.body.decode('utf-8'))
        models.ossconf.objects.update_or_create(id=res['id'],defaults=res)

        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
    return JsonResponse(settings.RESULT)

def baseConfig(request):
    if request.method == 'POST' or request.method == 'post':
        res = json.loads(request.body.decode('utf-8'))
        try:
            models.baseConfig.objects.create(**res)
            settings.RESULT['code'] = 2001
            settings.RESULT['msg'] = 'success'
        except Exception as e:
            settings.RESULT['code'] = 2006
            settings.RESULT['msg'] = 'fail'
            settings.RESULT['data'] = str(e)
        return JsonResponse(settings.RESULT)

    if request.method == 'GET' or request.method == 'get':
        res = models.baseConfig.objects.all().values()
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        settings.RESULT['count'] = res.count()
        settings.RESULT['data'] = list(res)
        return JsonResponse(settings.RESULT)

    if request.method == 'PUT' or request.method == 'put':
        res = json.loads(request.body.decode('utf-8'))
        models.baseConfig.objects.filter(pk=res['id']).update(**res)
        settings.finalData['code'] = 2001
        settings.finalData['msg'] = 'success'
        return JsonResponse(settings.finalData)





## 邮件配置相关
def mailserver(request):
    pass


def changemailserver(request):
    if request.method == 'POST':
        res = request.body.decode('utf-8')
        print(res)

    return HttpResponse('success')






def Aescrypt(reqsecret, type):
    back_data = {}
    passKey=models.baseConfig.objects.filter(confKey='passKey').values('confValue').first()['confValue']
    passOffset=models.baseConfig.objects.filter(confKey='passOffset').values('confValue').first()['confValue']

    ###这里初始化加密对象 传入key 初始化密钥, 以及对应的偏移量
    text = midplatformcrypt.midowncrppt(passKey, passOffset)
    if int(type) == 0:
        e = text.encrypt(reqsecret)

        back_data['jiami'] = e.decode('utf-8')
    else:
        jie_mi = text.decrypt(reqsecret)
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
        if sysUserType == None:
            return JsonResponse({'code': 2002, 'msg': 'fail', 'data': 'type未必传参数'})
        limit = int(request.GET.get('limit', default=10))
        page = int(request.GET.get('page', default=1))
        username = request.GET.get('username')
        nickname = request.GET.get('nickname')
        phone = request.GET.get('phone')
        kwargs = {
            ##动态查询条件
        }
        if username != None:
            kwargs['username'] = username
        if nickname != None:
            kwargs['nickname'] = nickname
        if phone != None:
            kwargs['phone'] = phone

        sysUser = models.sys_user.objects.filter(type__gte=sysUserType, deleted=0).filter(**kwargs).order_by(
            '-createTime').values('id', 'username', 'nickname', 'password', 'salt', 'avatar', 'gender', 'email',
                                  'phone', 'status', 'type', 'deleted', 'createTime', 'updateTime')
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
        id = int(request.get_full_path().split('?')[1].split('=')[1])
        import datetime
        deltime = datetime.datetime.now().strftime('%b-%d-%y %H:%M:%S')
        models.sys_user.objects.filter(pk=id).update(deleted=deltime)
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'


    elif request.method == 'PUT' or request.method == 'put':
        res = json.loads(request.body.decode('utf-8'))
        if 'avatar' in res.keys() and res['avatar'] != None:
            if res['avatar'].split('/')[0] != 'midplatform':
                avatarPath = ossupload.uploadBase64Pic(res['avatar'])
                if avatarPath != None:
                    res['avatar'] = avatarPath
                else:
                    settings.RESULT['code'] = 2002
                    settings.RESULT['msg'] = 'fail'
                    return JsonResponse(settings.RESULT)
        models.sys_user.objects.filter(pk=res['id']).update(**res)
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'

    elif request.method == 'POST' or request.method == 'post':
        sysUserDict = json.loads(request.body.decode('utf-8'))
        if 'avatar'  in sysUserDict:
            if sysUserDict['avatar'] != None:
                avatarPath = ossupload.uploadBase64Pic(sysUserDict['avatar'])
                if avatarPath != None:
                    sysUserDict['avatar'] = avatarPath
                else:
                    settings.RESULT['code'] = 2002
                    settings.RESULT['msg'] = 'fail'
                    return JsonResponse(settings.RESULT)
        try:
            models.sys_user.objects.create(**sysUserDict)
            settings.RESULT['code'] = 2001
            settings.RESULT['msg'] = 'success'
        except Exception as e:
            settings.RESULT['code'] = 2009
            settings.RESULT['msg'] = '用户已存在'
            settings.RESULT['data'] = str(e)

    return JsonResponse(settings.RESULT)


###系统用户授权
def sysusergrant(request):
    if request.method == 'GET' or request.method == 'get':
        id = request.GET.get('id')
        res = models.sys_user_role.objects.filter(user_id=id).values('role_id')
        return JsonResponse({"code": 2001, "msg": "success", "data": {"roleIds": list(res)}})

    if request.method == 'PUT' or request.method == 'put':
        res = json.loads(request.body.decode('utf-8'))

        roleIds = res['roleIds']

        if roleIds == None:
            return JsonResponse({'code': 2002, 'msg': 'fail', 'data': '授权ID为空'})
        else:
            # for i in roleIds:
            object, created = models.sys_user_role.objects.update_or_create(user_id=res['userId'], role_id=roleIds)
            print(object, created)
            ##这里去更新用户表的字段type 区分类型
            models.sys_user.objects.filter(pk=res['userId']).update(type=roleIds)
        return JsonResponse({'code': 2001, 'msg': 'success'})


def sysRoleSelect(request):
    if request.method == 'GET' or request.method == 'get':
        res = models.sys_role.objects.values('name', 'id')
        return JsonResponse({'code': 2000, 'msg': 'success', 'data': list(res)})


def sysRoleMenuSelect(request):
    if request.method == 'GET' or request.method == 'get':
        id = request.GET.get('id')
        res = models.sys_role_menu.objects.filter(role_id=id).values_list('permission_id', flat=True)
        return JsonResponse({"code": 2001, "msg": "success", "data": list(res)})

    if request.method == 'PUT' or request.method == 'put':
        res = json.loads(request.body.decode('utf-8'))
        permissionId = res['permissionId']

        if len(permissionId) == 0:
            return JsonResponse({'code': 2002, 'msg': 'fail', 'data': '授权ID为空'})
        else:
            models.sys_role_menu.objects.filter(role_id=res['id']).delete()
            for i in permissionId:
                models.sys_role_menu.objects.create(role_id=res['id'], permission_id=i)
        return JsonResponse({'code': 2001, 'msg': 'success'})


def setPassword(request):
    res = json.loads(request.body.decode('utf-8'))
    if request.method == 'PUT' or request.method == 'put':
        if 'id' not in res.keys():
            return JsonResponse({'code': 2002, 'msg': 'fail', 'data': '未携带用户ID'})
        if res['password'] == res['confirm']:
            crypt = Aescrypt(res['password'], 1)
            models.sys_user.objects.filter(pk=res['id']).update(password=crypt['jiemi'])
            return JsonResponse({'code': 2001, 'msg': 'success'})
        else:
            return JsonResponse({'code': 2002, 'msg': 'fail', 'data': '两次输入密码不一致'})


def sysRole(request):
    if request.method == 'GET' or request.method == 'get':
        code = request.GET.get('code')
        name = request.GET.get('name')
        kwargs2 = {}
        if code != None:
            kwargs2['code'] = code
        if name != None:
            kwargs2['name'] = name
        kwargs2['deleted'] = 0
        res = models.sys_role.objects.filter(**kwargs2).values()
        settings.finalData['code'] = 2001
        settings.finalData['msg'] = 'success'
        settings.finalData['data'] = list(res)

        return JsonResponse(settings.finalData)

    kwargs = {
        ###动态参数拼接
    }
    res = json.loads(request.body.decode('utf-8'))
    if 'code' in res.keys() and res['code'] != None:
        kwargs['code'] = res['code']
    if 'name' in res.keys() and res['name'] != None:
        kwargs['name'] = res['name']
    if 'note' in res.keys() and res['note'] != None:
        kwargs['note'] = res['note']
    try:
        if request.method == 'POST' or request.method == 'post':
            models.sys_role.objects.create(**kwargs)

        if request.method == 'PUT' or request.method == 'put':
            ###编辑角色，必须带有ID
            models.sys_role.objects.filter(pk=res['id']).update(**kwargs)
        if request.method == 'DELETE' or request.method == 'delete':
            id = int(request.get_full_path().split('?')[1].split('=')[1])
            models.sys_role.objects.filter(id=id).update(deleted=1)


    except:
        return JsonResponse({'code': 2001, 'msg': 'success'})

    return JsonResponse({'code': 2001, 'msg': 'success'})


def sysuserlogin(request):

    param_dict = {}
    if request.method == 'POST' or request.method == 'post':
        query_param = request.get_full_path().split('?')[1]
        res = query_param.split('&')
        for i in res:
            param_dict[i.split('=')[0]] = i.split('=')[1]
    originPassword = Aescrypt(param_dict['password'], 1)['jiemi']
    res = models.sys_user.objects.filter(username=param_dict['username']).count()
    if res == 0:
        return JsonResponse({'code': 2003, 'msg': 'fail', 'data': '用户不存在'})

    dbPassword = model_to_dict(models.sys_user.objects.filter(username=param_dict['username']).first())['password']
    print(dbPassword,originPassword)
    if originPassword == dbPassword:
        info =model_to_dict(models.sys_user.objects.get(username=param_dict['username']))
        info['password'] = Aescrypt(info['password'],0)['jiami']

        ###获取用户对应角色的权限
        user_role_id= model_to_dict(models.sys_user_role.objects.filter(user_id=int(info['id'])).first())['role_id']

        user_persssions_id = list(models.sys_role_menu.objects.filter(role_id=user_role_id).values_list('permission_id',flat=True))

        ###查询当前用户的角色 ROLE_DEV ROLE_ADMIN 等等
        roles = models.sys_role.objects.filter(id=user_role_id).values_list('code',flat=True)

        permissions = models.sys_menu.objects.filter(id__in=user_persssions_id).values_list('code',flat=True)

        from common import tokenserver
        access_token = tokenserver.create_token(param_dict['username'])
        settings.loginDic['access_token'] =access_token
        settings.loginDic['expires_in'] =1800
        settings.loginDic['permissions'] = list(permissions)
        settings.loginDic['roles'] = list(roles)
        settings.loginDic['info'] = info
        # print(settings.loginDic)
        return JsonResponse({'code': 2001, 'msg': 'success', 'data':settings.loginDic})
    return JsonResponse({'code': 2004, 'msg': 'fail', 'data': '密码错误'})



def codeMsg(request):
    if request.method == 'GET' or request.method == 'get':
        return JsonResponse(settings.codeMsg)

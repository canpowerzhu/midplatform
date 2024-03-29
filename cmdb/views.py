from django.http import JsonResponse
from django.db.models import Sum, FloatField
import json
from common import baseconfig
from common.logconf import get_log_insert
from midplatform import settings
from cmdb import models as cmdbmodels
from common.aliyun import instance

accesskeyId = baseconfig.getconfig()['accessKey']
accessSecret = baseconfig.getconfig()['accessSecret']

from django.core.paginator import Paginator


# 可用区相关
def region(request):
    """
    type
    0-同步region信息
    1-同步region下的ecs信息

    :param request:
    :return:
    """

    if request.method == 'GET' or request.method == 'get':
        res = list(cmdbmodels.region.objects.all().values())
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        settings.RESULT['count'] = len(res)
        settings.RESULT['data'] = res
        return JsonResponse(settings.RESULT)
    if request.method == 'PUT' or request.method == 'put':
        res = json.loads(request.body.decode('utf-8'))
        get_log_insert.logrecord(1, request, {'msg': '修改本地region,格式化名' + res['humanName']})
        cmdbmodels.region.objects.filter(pk=int(res['id'])).update(humanName=res['humanName'])
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'

        return JsonResponse(settings.RESULT)

    if request.method != 'POST':
        settings.RESULT['code'] = 405
        settings.RESULT['msg'] = 'fail'
        settings.RESULT['data'] = '请使用post请求'
        return JsonResponse(settings.RESULT)

    # 同步对应region的实例
    # 资产同步接口
    if request.method == 'POST' or request.method == 'post':
        resqBody = json.loads(request.body.decode('utf-8'))
        from common.aliyun import region
        if resqBody['type'] == 0:

            res = region.syncregion(resqBody)
            info = "同步可用区 [" + resqBody['regionId'] + "] 下面的所有实例"
            get_log_insert.logrecord(1, request, {'msg': info})
        else:
            res = region.syncall()
        return JsonResponse(res)


# 资产组相关
def assetgroup(request):
    # 定义空字典
    if request.method == 'POST' or request.method == 'post':

        res = json.loads(request.body.decode('utf-8'))

        try:
            object, created = cmdbmodels.assetGroup.objects.update_or_create(name=res['name'],
                                                                             defaults={'name': res['name'],
                                                                                       'comment': res['comment']})
            if created:
                settings.RESULT['data'] = '新增成功'
                info = "新增资产组 [" + res['name'] + "]"

            else:
                info = "修改资产组 [" + res['name'] + "]"
                settings.RESULT['data'] = '修改成功'
            get_log_insert.logrecord(1, request, {'msg': info})
            settings.RESULT['code'] = 2001
            settings.RESULT['msg'] = 'success'
        except Exception as e:
            settings.RESULT['code'] = '2009'
            settings.RESULT['msg'] = 'fail'
            settings.RESULT['data'] = str(e)

        return JsonResponse(settings.RESULT)

    if request.method == 'DELETE' or request.method == 'delete':
        delid = request.GET.get('id')
        regionGroupName = cmdbmodels.assetGroup.objects.filter(pk=int(delid)).values().first()['name']
        info = "删除资产组 [" + regionGroupName + "]"
        get_log_insert.logrecord(1, request, {'msg': info})
        cmdbmodels.assetGroup.objects.filter(pk=int(delid)).delete()
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        return JsonResponse(settings.RESULT)

    if request.method == 'GET' or request.method == 'get':
        res = list(cmdbmodels.assetGroup.objects.all().values())
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        settings.RESULT['count'] = len(res)
        settings.RESULT['data'] = res
        return JsonResponse(settings.RESULT)

    if request.method == 'PUT' or request.method == 'put':
        res = json.loads(request.body.decode('utf-8'))
        orginInfo = list(cmdbmodels.assetGroup.objects.filter(pk=res['id']).values())[0]
        info = "变更资产组 由" + str(orginInfo) + " 更改为" + str(res)
        get_log_insert.logrecord(1, request, {'msg': info})
        cmdbmodels.assetGroup.objects.filter(pk=res['id']).update(name=res['name'], comment=res['comment'])
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'

        return JsonResponse(settings.RESULT)


# 资产实例
def asset(request):
    ## 此接口主要用于实例的启动停止 重启功能
    if request.method == 'PUT' or request.method == 'put':
        # 获取要进行的实例的动作 0 - stop 1-start 2-restart
        doaction = json.loads(request.body.decode('utf-8'))
        InstanceId = doaction['instanceId']
        action = doaction['action']

        # 实例ID 必须存在
        res = cmdbmodels.asset.objects.filter(instanceId=InstanceId)
        if not res.exists():
            settings.RESULT['code'] = 2009
            settings.RESULT['msg'] = 'fail'

        cur_ecs_status = res.values('status').first()['status']
        # 如果停止0  必须状态为running  0
        if (action == 0 and cur_ecs_status == 0) or (
                action == 1 and cur_ecs_status == 3) or (
                action == 2 and cur_ecs_status == 0):
            modifyres = instance.InstanceStatus(res.values('regionId').first()['regionId'], InstanceId, action)
            # 上述完成后我们要去更新数据库数据
            info = "实例" + InstanceId + "状态更改为" + str(action)
            get_log_insert.logrecord(1, request, {'msg': info})
            print(InstanceId, action, modifyres)
            cmdbmodels.asset.objects.filter(instanceId=InstanceId).update(status=modifyres)
            settings.RESULT['code'] = 2001
            settings.RESULT['msg'] = 'success'
            settings.RESULT['data'] = '操作成功'
        else:
            settings.RESULT['code'] = 2009
            settings.RESULT['msg'] = 'fail'
            settings.RESULT['data'] = '操作失败'

        return JsonResponse(settings.RESULT)

    if request.method == 'GET' or request.method == 'get':
        limit = request.GET.get('limit', default=200)
        page = request.GET.get('page', default=1)
        kwargs = {}
        instanceName = request.GET.get('instanceName')
        publicIp = request.GET.get('publicIp')

        if publicIp:
            kwargs['publicIp'] = publicIp

        if instanceName:
            kwargs['instanceName'] = instanceName

        if (not publicIp) and (not instanceName):
            res = cmdbmodels.asset.objects.all().values()
        else:
            res = cmdbmodels.asset.objects.filter(**kwargs).values()
        assetlist = Paginator(res, limit)  # 进行分页
        page_asset = assetlist.page(page)  # 返回对应页码
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        settings.RESULT['data'] = list(page_asset)
        settings.RESULT['count'] = res.count()

        return JsonResponse(settings.RESULT)


# 弹性IP
# 同步、解绑、绑定、释放、购买 post
# 升级更新 put

def eipinfo(request):
    if request.method == 'post' or request.method == 'POST':
        from common.aliyun import eip
        actionType = {
            0: eip.syncEip,  # 同步对应region 的弹性IP
            1: eip.buyEip,  # 购买EIP
            2: eip.associateEip,  # 绑定EIP
            3: eip.unassociateEip,  # 解绑EIP
            4: eip.releaseEip,  # 释放EIP
            5: eip.modifyEip  # 升级更新EIP
        }
        resbody = json.loads(request.body.decode('utf-8'))
        actionTypeInt = resbody['type']
        respData = actionType[actionTypeInt](resbody)  # 这是去执行对应的方法
        return JsonResponse(respData)

    if request.method == 'get' or request.method == 'GET':
        data = cmdbmodels.eip.objects.all().values()
        limit = request.GET.get('limit', default=10)
        page = request.GET.get('page', default=1)

        assetlist = Paginator(data, limit)  # 进行分页
        page_asset = assetlist.page(page)  #
        count = data.count()
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        settings.RESULT['data'] = list(page_asset)
        settings.RESULT['count'] = count
        return JsonResponse(settings.RESULT)


# 资产组
# 移出资产组，加入资产组，罗列资产组,同步资产组

def resourceGroup(request):
    from common.aliyun import resourceGroup
    if request.method == 'POST' or request.method == 'post':
        # 移出资产组、加入资产组、同步资产组
        actionType = {
            0: resourceGroup.syncResourceGroup,
            1: resourceGroup.joinResourceGroup,
            2: resourceGroup.removeResourceGroup,
            3: resourceGroup.assetForReourceGroup,
        }

        reqBody = json.loads(request.body.decode('utf-8'))
        if reqBody['type'] in actionType.keys():
            respData = actionType[reqBody['type']]()

            return JsonResponse(respData)
        else:
            settings.RESULT['code'] = 2009
            settings.RESULT['msg'] = 'fail'
            settings.RESULT['data'] = 'type；类型不存在'
            return JsonResponse(settings.RESULT)

    if request.method == 'GET' or request.method == 'get':
        # 罗列资产组
        respdata = resourceGroup.listResourceGroup()
        return JsonResponse(respdata)


# 账单相关
def billmonth(request):
    from common.aliyun import bill
    if request.method == 'post' or request.method == 'POST':
        resqBody = json.loads(request.body.decode('utf-8'))
        pagesize = resqBody['pagesize']
        billingCycle = resqBody['billingCycle']
        respdata = bill.syncMonthBill(billingCycle, pagesize)
        info = "同步" + billingCycle + "的账单"
        # get_log_insert.logrecord(1, request, {'msg': info})
        return JsonResponse(respdata)

    if request.method == 'GET' or request.method == 'get':

        import datetime,arrow
        defaultPeriod = arrow.now().shift(months=-1).format("YYYY-MM-01")
        lastPeriod = arrow.now().shift(months=-2).format("YYYY-MM-01")
        sixPeriod = arrow.now().shift(months=-6).format("YYYY-MM-01")


        # 账单时间
        billingPeriod = request.GET.get('billingPeriod')
        if billingPeriod:
            billingarrow=arrow.get(int(billingPeriod.split('-')[0]),int(billingPeriod.split('-')[1]),1)
            allperiod = billingarrow.format("YYYY-MM-01")
            lastPeriod=billingarrow.shift(months=-1).format("YYYY-MM-01")
            sixPeriod = billingarrow.shift(months=-6).format("YYYY-MM-01")
        else:
            allperiod = defaultPeriod
            lastPeriod = lastPeriod


        # 获取依据groupname 判断业务类型
        groupBy = request.GET.get('groupname')
        if groupBy:
            # 用于饼状图和table图
            groupName = groupBy
            if groupName == 'resourceGroup':
                res = cmdbmodels.billDetail.objects.filter(billingCycle=allperiod).values('resourceGroup',
                    'billingCycle').annotate(total=Sum('pretaxAmount', output_field=FloatField())).order_by('-total')

                for i in list(res):
                    lastcost = cmdbmodels.billDetail.objects.filter(resourceGroup=i['resourceGroup'],billingCycle=lastPeriod).aggregate(
                        nums=Sum('pretaxAmount', output_field=FloatField()))
                    i['lastcost'] = lastcost['nums']
                    if lastcost['nums'] == None:
                        i['rate'] = 0.00
                    else:
                        i['rate'] = round((i['total'] - lastcost['nums']) / lastcost['nums'], 2)
            elif groupName == 'productDetail':
                res = cmdbmodels.billDetail.objects.filter(billingCycle=allperiod).values('productDetail',
                                                                                                  'billingCycle').annotate(
                    total=Sum('pretaxAmount', output_field=FloatField())).order_by('-total')
            settings.RESULT['data'] = list(res)
            settings.RESULT['count'] = res.count()

        else:

            groupName = 'billingCycle'
            # 这是获取近六个月的账单,用于柱状图
            endDate = sixPeriod
            daterange = cmdbmodels.billDetail.objects.filter(billingCycle__gte=endDate).filter(billingCycle__lte=allperiod).values('billingCycle').distinct()
            finallist = []
            for i in range(daterange.count()):
                period = list(daterange)[i]['billingCycle']
                perdata = cmdbmodels.billDetail.objects.filter(billingCycle=list(daterange)[i]['billingCycle']).values(
                    'productDetail').annotate(subtotal=Sum('pretaxAmount', output_field=FloatField()))
                for j in range(perdata.count()):
                    # 组装数据格式
                    list(perdata)[j]['period'] = period.strftime("%Y-%m")
                    finallist.append(perdata[j])

            settings.RESULT['data'] = finallist
            settings.RESULT['count'] = len(finallist)

        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        settings.RESULT['period'] = allperiod
        settings.RESULT['groupname'] = groupName

        return JsonResponse(settings.RESULT)

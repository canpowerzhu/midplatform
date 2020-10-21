# @Author  : kane.zhu
# @Time    : 2020/9/2 16:25
# @Software: PyCharm
# 此模块主要操作弹性IP
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkvpc.request.v20160428.AllocateEipAddressRequest import AllocateEipAddressRequest
from aliyunsdkvpc.request.v20160428.UnassociateEipAddressRequest import UnassociateEipAddressRequest
from aliyunsdkvpc.request.v20160428.AssociateEipAddressRequest import AssociateEipAddressRequest
from aliyunsdkvpc.request.v20160428.ModifyEipAddressAttributeRequest import ModifyEipAddressAttributeRequest
from aliyunsdkvpc.request.v20160428.ReleaseEipAddressRequest import ReleaseEipAddressRequest
from aliyunsdkvpc.request.v20160428.DescribeEipAddressesRequest import DescribeEipAddressesRequest
from cmdb import models as cmdbmodels
import json,datetime
from midplatform import  settings
from common import baseconfig


accesskeyId = baseconfig.getconfig()['accessKey']
accessSecret = baseconfig.getconfig()['accessSecret']



def buyEip(data):

    if 'resourceGroupId' not in data or  'bandWidth' not in data or 'chargeType' not in data or 'regionId' not in data:
        settings.RESULT['code'] = 2009
        settings.RESULT['msg'] = 'fail'
        settings.RESULT['data'] = '缺少必填参数'
        return settings.RESULT

    # 这边同一判断ISP 线路类型 预付费和按量付费都是一样的条件
    if data['isp'] == 1 and data['regionId'] == 'cn-hongkong':
        ISP = 'BGP_PRO'
    else:
        ISP = 'BGP'

    client = AcsClient(accesskeyId, accessSecret, data['regionId'])
    request = AllocateEipAddressRequest()
    request.set_accept_format('json')
    request.set_ResourceGroupId(data['resourceGroupId'])
    request.set_ISP(ISP)
    request.set_Bandwidth(data['bandWidth'])




    if data['chargeType'] == 1:
        # chargeType 是1 则是预付费 包年包月类型
        print(data['period'])
        if  data['period']  not in range(1,9) or data['bandWidth'] not in range(1,1000):
            settings.RESULT['code'] = 2009
            settings.RESULT['msg'] = 'fail'
            settings.RESULT['data'] = '选择的购买时长(period)参数异常'
            return  settings.RESULT



        request.set_Period(int(data['period']))
        request.set_AutoPay(True)
        request.set_InstanceChargeType('PrePaid')
        request.set_InternetChargeType('PayByBandwidth')
        response = client.do_action_with_exception(request)



    if data['chargeType'] == 0:
        # chargeType 0 是按量付费
        print(data['bandWidth'])
        if data['bandWidth'] not in range(1, 500)  or 'internetChargeType'  not in data:
            settings.RESULT['code'] = 2009
            settings.RESULT['msg'] = 'fail'
            settings.RESULT['data'] = '(bandWidth取值区间[1,500],internetChargeType)参数异常'
            return settings.RESULT
        if data['internetChargeType'] == 0:
            internetChargeType = 'PayByBandwidth'
        else:
            internetChargeType = 'PayByTraffic'
        request.set_InstanceChargeType('PostPaid')
        request.set_InternetChargeType(internetChargeType)
        response = client.do_action_with_exception(request)

    settings.RESULT['code'] = 2001
    settings.RESULT['msg'] = 'success'
    settings.RESULT['data'] = str(response, encoding='utf-8')
    return settings.RESULT





#释放EIP
def releaseEip(data):
    if 'regionId' not in data or 'allocationId' not in data:
        settings.RESULT['code'] = 2009
        settings.RESULT['msg'] = 'fail'
        return settings.RESULT
    client = AcsClient(accesskeyId, accessSecret, data['regionId'])
    request = ReleaseEipAddressRequest()
    request.set_accept_format('json')
    request.set_AllocationId(data['allocationId'])
    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))
    settings.RESULT['code'] = 2001
    settings.RESULT['msg'] = 'success'
    return settings.RESULT


# 解绑EIP
def unassociateEip(data):
    if  'regionId' not in data or  'allocationId' not in data:
        settings.RESULT['code'] = 2009
        settings.RESULT['msg'] = 'fail'
        return  settings.RESULT
    client = AcsClient(accesskeyId, accessSecret, data['regionId'])
    request = UnassociateEipAddressRequest()
    request.set_accept_format('json')

    request.set_AllocationId(data['allocationId'])
    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))
    settings.RESULT['code'] = 2001
    settings.RESULT['msg'] = 'success'
    return settings.RESULT

# 绑定EIP
def associateEip(data):

    if  'regionId' not in data or 'instanceId' not in data or 'allocationId' not in data:
        settings.RESULT['code'] = 2009
        settings.RESULT['msg'] = 'fail'
        return  settings.RESULT


    client = AcsClient(accesskeyId, accessSecret, data['regionId'])
    request = AssociateEipAddressRequest()
    request.set_accept_format('json')
    request.set_InstanceId(data['instanceId'])
    request.set_AllocationId(data['allocationId'])
    try:
        response = client.do_action_with_exception(request)
        print(str(response, encoding='utf-8'))
    except ServerException as e:
        print(e.get_error_code())
        print(e.get_error_msg())
        print(e.get_error_type())
    except ClientException as e:
        print(e)
    settings.RESULT['code'] = 2001
    settings.RESULT['msg'] = 'success'
    return settings.RESULT

# 修改规格
def modifyEip(data):

    client = AcsClient(accesskeyId, accessSecret, data['regionId'])
    request = ModifyEipAddressAttributeRequest()
    request.set_accept_format('json')
    request.set_AllocationId(data['allocationId'])
    if 'bandWidth' in data:
        request.set_Bandwidth(data['bandWidth'])

    if 'description' in data:
        request.set_Description(data['description'])
    if 'name' in data:
        request.set_Name(data['name'])

    try:
        response = client.do_action_with_exception(request)
    except ServerException as e:
        print(e.get_error_code())
        print(e.get_error_msg())
        print(e.get_error_type())
    except ClientException as e:
        print(e)

    settings.RESULT['code'] = 2001
    settings.RESULT['msg'] = 'success'
    return  settings.RESULT


# 同步对应region的eip
def  syncEip(data):
    regionId = data['regionId']
    client = AcsClient(accesskeyId, accessSecret, regionId)
    request = DescribeEipAddressesRequest()
    request.set_accept_format('json')
    response = json.loads(str(client.do_action_with_exception(request), encoding='utf-8'))

    getdatalist = response['EipAddresses']['EipAddress']
    getdatacount = response['TotalCount']
    eipList=[]
    for i in range(getdatacount):
        perdata = getdatalist[i]
        # 判断ISP类型

        if perdata['ISP'] == 'BGP_PRO':
            isp=1
        else:
            isp=0


        # 判断使用状态
        if perdata['Status'] == 'InUse':
            status = 1
        else:
            status = 0


        # 判断付费类型
        if perdata['ChargeType'] == 'PostPaid':
            chargeType=0
        else:
            chargeType=1

        # 计费类型
        if perdata['InternetChargeType'] == 'PayByBandwidth':
            internetChargeType=0 #带宽付费
        else:
            internetChargeType=1 #流量付费

        eipList.append(perdata['InstanceId'])
        object,created = cmdbmodels.eip.objects.update_or_create(allocationId=perdata['AllocationId'],
                                                defaults={'regionId':perdata['RegionId'],
                                                          'allocationId':perdata['AllocationId'],
                                                          'allocationName':perdata['Name'],
                                                          'instanceId':perdata['InstanceId'],
                                                          'resourceGroupId':perdata['ResourceGroupId'],
                                                          'bandWidth':perdata['Bandwidth'],
                                                          'isp':isp,
                                                          'eipAdress':perdata['IpAddress'],
                                                          'eipstatus':status,
                                                          'chargeType':chargeType,
                                                          'internetChargeType':internetChargeType,
                                                          'createTime':datetime.datetime.strptime(
                                                              perdata['AllocationTime'],
                                                              "%Y-%m-%dT%H:%M:%SZ")})

        # 这里需要注意 前提条件 在同一regionId的情况下
    cmdbmodels.eip.objects.filter(regionId=perdata['RegionId']).exclude(instanceId__in=eipList).delete()
    res = cmdbmodels.eip.objects.all().values()
    settings.RESULT['code'] = 2001
    settings.RESULT['msg'] = 'success'
    settings.RESULT['count'] = getdatacount
    settings.RESULT['data'] = list(res)
    print(settings.RESULT)
    return settings.RESULT
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

import json

from common import baseconfig


accesskeyId = baseconfig.getconfig()['accessKey']
accessSecret = baseconfig.getconfig()['accessSecret']



def buyEip(regionId,Bandwidth,):
    client = AcsClient(accesskeyId, accessSecret, 'ap-southeast-1')
    request = AllocateEipAddressRequest()
    request.set_accept_format('json')
    response = client.do_action_with_exception(request)

#释放EIP
def releaseEip(regionId,allocationId):
    client = AcsClient(accesskeyId, accessSecret, regionId)
    request = ReleaseEipAddressRequest()
    request.set_accept_format('json')
    request.set_AllocationId(allocationId)
    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))


# 解绑EIP
def unassociateEip(regionId,instanceId,allocationId):
    client = AcsClient(accesskeyId, accessSecret, regionId)
    request = UnassociateEipAddressRequest()
    request.set_accept_format('json')
    request.set_InstanceId(instanceId)
    request.set_AllocationId(allocationId)
    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))


# 绑定EIP
def associateEip(regionId,instanceId,allocationId):
    client = AcsClient(accesskeyId, accessSecret, regionId)
    request = AssociateEipAddressRequest()
    request.set_accept_format('json')
    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))


# 修改规格
def modifyEip(regionId,bandwidth,allocaitonId):
    client = AcsClient(accesskeyId, accessSecret, regionId)
    request = ModifyEipAddressAttributeRequest()
    request.set_accept_format('json')
    request.set_Bandwidth(bandwidth)
    request.set_AllocationId(allocaitonId)
    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))


# 同步对应region的eip
def  syncEip(data):
    regionId = data['regionId']
    client = AcsClient(accesskeyId, accessSecret, regionId)
    request = DescribeEipAddressesRequest()
    request.set_accept_format('json')
    response = json.loads(str(client.do_action_with_exception(request), encoding='utf-8'))

    print(type(response))
    getdatalist = response['EipAddresses']['EipAddress']
    getdatacount = response['TotalCount']
    for i in range(getdatacount):
        print(getdatalist[i])
    # print(str(response, encoding='utf-8'))
    return {'status':'ok','type':2}
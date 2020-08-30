# @Author  : kane.zhu
# @Time    : 2020/8/28 11:25
# @Software: PyCharm


from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeRegionsRequest import DescribeRegionsRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526.StopInstanceRequest import StopInstanceRequest
from aliyunsdkecs.request.v20140526.StartInstanceRequest import StartInstanceRequest
from aliyunsdkecs.request.v20140526.RebootInstanceRequest import RebootInstanceRequest
from aliyunsdkecs.request.v20140526.DescribeInstanceAttributeRequest import DescribeInstanceAttributeRequest


import json

from common import baseconfig


accesskeyId = baseconfig.getconfig()['accessKey']
accessSecret = baseconfig.getconfig()['accessSecret']
#定义实例状态字典
ecsstatusdict = {
            'Running': 0,
            'Starting': 1,
            'Stopping': 2,
            'Stopped': 3
        }

# 同步region信息
def SyncRegion():
    client = AcsClient(accesskeyId, accessSecret, 'cn-hangzhou')
    request = DescribeRegionsRequest()
    request.set_accept_format('json')
    response = json.loads(client.do_action_with_exception(request), encoding='utf-8')
    return  response



# 同步实例信息
def InstanceSync(regionId,pageSize,pageNum):
    client = AcsClient(accesskeyId, accessSecret, regionId)
    request = DescribeInstancesRequest()
    request.set_accept_format('json')
    request.set_PageSize(int(pageSize))
    request.set_PageNumber(int(pageNum))
    response = client.do_action_with_exception(request)
    data = json.loads(str(response, encoding='utf-8'))
    return  data


def InstanceStatus(regionId,instanceId,type):
    typedict ={
        0:StopInstanceRequest,
        1:StartInstanceRequest,
        2:RebootInstanceRequest
    }
    client = AcsClient(accesskeyId, accessSecret, regionId)
    print(typedict[int(type)])
    request = typedict[int(type)]()




    request.set_accept_format('json')

    request.set_InstanceId(instanceId)


    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))
    #获取实例状态
    import time
    time.sleep(5)
    getInstanceInfo = DescribeInstanceAttributeRequest()
    getInstanceInfo.set_accept_format('json')
    getInstanceInfo.set_InstanceId(instanceId)
    ecsstatus = json.loads(client.do_action_with_exception(getInstanceInfo))
    print(ecsstatus)

    return 0
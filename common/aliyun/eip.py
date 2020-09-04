# @Author  : kane.zhu
# @Time    : 2020/9/2 16:25
# @Software: PyCharm
# 此模块主要操作弹性IP
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.AllocateEipAddressRequest import AllocateEipAddressRequest

import json

from common import baseconfig


accesskeyId = baseconfig.getconfig()['accessKey']
accessSecret = baseconfig.getconfig()['accessSecret']



def buyEip(regionId,Bandwidth,):
    client = AcsClient(accesskeyId, accessSecret, 'ap-southeast-1')

    request = AllocateEipAddressRequest()
    request.set_accept_format('json')

    response = client.do_action_with_exception(request)
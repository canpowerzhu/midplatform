# @Author  : kane.zhu
# @Time    : 2020/9/8 21:43
# @Software: PyCharm

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkresourcemanager.request.v20200331.ListResourceGroupsRequest import ListResourceGroupsRequest

from cmdb import models as cmdbmodels
from common import baseconfig
from midplatform import  settings
import json,datetime

accesskeyId = baseconfig.getconfig()['accessKey']
accessSecret = baseconfig.getconfig()['accessSecret']

# 罗列资产组
def listResourceGroup():
    getdata =cmdbmodels.resourceGroup.objects.all().values()
    settings.RESULT['code']= 2001
    settings.RESULT['msg']= 'success'
    settings.RESULT['data']= list(getdata)
    settings.RESULT['count']= getdata.count()
    return  settings.RESULT



#同步资产组
def syncResourceGroup():
    client = AcsClient(accesskeyId, accessSecret, 'cn-hangzhou')
    request = ListResourceGroupsRequest()
    request.set_accept_format('json')

    request.set_PageSize(100)
    try:
        response = json.loads(str(client.do_action_with_exception(request),encoding='utf-8'))
        getdata= response['ResourceGroups']['ResourceGroup']
        getdatacount = response['TotalCount']
        resourceGroupIdLits=[]
        for i in range(getdatacount):
            resourceGroupIdLits.append(getdata[i]['Id'])
            cmdbmodels.resourceGroup.objects.update_or_create(resourceId=getdata[i],defaults={
                'name':getdata[i]['Name'],
                'resourceId':getdata[i]['Id'],
                'accountId':getdata[i]['AccountId'],
                'status':getdata[i]['Status'],
                'displayName':getdata[i]['DisplayName'],
                'createTime':datetime.datetime.strptime(getdata[i]['CreateDate'],
                                                              "%Y-%m-%dT%H:%M:%S+08:00"),

            })
        # 处理线上不存在，数据库存在的数据
        cmdbmodels.resourceGroup.objects.exclude(resourceId__in=resourceGroupIdLits).delete()
    except ClientException as e:
        print(e)
    except ServerException as e:
        print(e)


    settings.RESULT['code'] = 2001
    settings.RESULT['msg'] = 'success'

    return settings.RESULT

# 移出资产组
def removeResourceGroup():
    pass

# 加入资产组
def joinResourceGroup():
    pass


# 罗列资产
def assetForReourceGroup():
    res = cmdbmodels.asset.objects.all().values('id','instanceId','instanceName')
    settings.RESULT['code'] = 2001
    settings.RESULT['msg'] = 'success'
    settings.RESULT['count'] = res.count()
    settings.RESULT['data'] = list(res)
    return settings.RESULT

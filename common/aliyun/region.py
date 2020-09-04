# @Author  : kane.zhu
# @Time    : 2020/9/4 16:43
# @Software: PyCharm
from common.aliyun import instance
from cmdb import models as cmdbmodels
import  datetime
from midplatform import settings
def syncregion(resqBody):
    data = instance.InstanceSync(resqBody['region'], resqBody['pageSize'], resqBody['pageNum'])
    for i in range(data['TotalCount']):
        instanceInfo = data['Instances']['Instance'][int(i)]

        # 判断是否有标签
        if instanceInfo.__contains__('Tags'):
            tagKey = instanceInfo['Tags']['Tag'][0]['TagKey']
            tagValue = instanceInfo['Tags']['Tag'][0]['TagValue']
        else:
            tagKey = None
            tagValue = None

        # 判断是否有标签
        if instanceInfo.__contains__('KeyPairName'):
            KeyPairName = instanceInfo['KeyPairName']
        else:
            KeyPairName = None

        # 判断实例网络类型 是vpc还是经典网络
        if instanceInfo['InstanceNetworkType'] == 'vpc':
            ipType = 1
            instanceNetworkType = 1
            privateIp = instanceInfo['VpcAttributes']['PrivateIpAddress']['IpAddress'][0]
            # 判断公网IP 是弹性IP 还是公网IP
            if len(instanceInfo['EipAddress']['IpAddress']) > 0:
                publicIp = instanceInfo['EipAddress']['IpAddress']
            else:
                publicIp = instanceInfo['PublicIpAddress']['IpAddress'][0]


        else:
            ipType = 0
            instanceNetworkType = 0
            # 这里的IP 是 经典网络  IP 数据取值第一个
            publicIp = instanceInfo['PublicIpAddress']['IpAddress'][0]
            privateIp = instanceInfo['InnerIpAddress']['IpAddress'][0]

        if instanceInfo['InstanceChargeType'] == 'PrePaid':
            ecsChargeType = 0
        else:
            ecsChargeType = 1

        if instanceInfo['OSType'] == 'linux':
            ostype = 1
        elif instanceInfo['OSType'] == 'windows':
            ostype = 0
        else:
            ostype = 2

        cmdbmodels.asset.objects.update_or_create(instanceId=instanceInfo['InstanceId'],
                                                  defaults={'instanceName': instanceInfo['InstanceName'],
                                                            'hostname': instanceInfo['HostName'],
                                                            'regionId': instanceInfo['RegionId'],
                                                            'status': instance.ecsstatusdict[
                                                                instanceInfo['Status']],
                                                            'keyPairName': KeyPairName,
                                                            'tagKey': tagKey,
                                                            'tagValue': tagValue,
                                                            'zoneId': instanceInfo['ZoneId'],
                                                            'instanceType': instanceInfo['InstanceType'],
                                                            'instanceNetworkType': instanceNetworkType,
                                                            'instanceChargeType': ecsChargeType,
                                                            'osType': ostype,
                                                            'osName': instanceInfo['OSName'],
                                                            'cpu': instanceInfo['Cpu'],
                                                            'memory': instanceInfo['Memory'],
                                                            'ipType': ipType,
                                                            'publicIp': publicIp,
                                                            'privateIp': privateIp,
                                                            'createTime': datetime.datetime.strptime(
                                                                instanceInfo['CreationTime'],
                                                                "%Y-%m-%dT%H:%MZ"),
                                                            'expiredTime': datetime.datetime.strptime(
                                                                instanceInfo['ExpiredTime'],
                                                                "%Y-%m-%dT%H:%MZ")})
    settings.RESULT['code'] = 2001
    settings.RESULT['msg'] = 'success'
    settings.RESULT['data'] = '同步完成'
    settings.RESULT['count'] = int(data['TotalCount'])
    return settings.RESULT



def syncall():
    res = instance.SyncRegion()
    regionlist = []
    for value in res['Regions']['Region']:
        regionlist.append(
            cmdbmodels.region(regionId=value['RegionId'],
                              regionEndpoint=value['RegionEndpoint'],
                              localName=value['LocalName']))
    try:
        cmdbmodels.region.objects.bulk_create(regionlist)
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
    except Exception as e:
        settings.RESULT['code'] = 2002
        settings.RESULT['msg'] = 'fail'
        settings.RESULT['data'] = str(e)
    return settings.RESULT
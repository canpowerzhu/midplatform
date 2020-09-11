from django.db.backends.mysql.base import DatabaseWrapper
DatabaseWrapper.data_types = DatabaseWrapper._data_types
# Create your models here.
from django.db import models

# region表
class region(models.Model):
    regionId = models.CharField(unique=True,max_length=200,verbose_name='regionid')
    regionEndpoint = models.CharField(max_length=200,verbose_name='regionEndpoint')
    localName = models.CharField(max_length=200,verbose_name='localName')
    humanName = models.CharField(blank=True,max_length=200,verbose_name='可读性高')


#资产组表
class assetGroup(models.Model):
    name = models.CharField(max_length=200,verbose_name='主机组名称')
    comment = models.CharField(blank=True,max_length=200,verbose_name='备注名称')

# 资产与主机组 以及region关系表
class asset_Group_Region(models.Model):
    assetId = models.IntegerField(blank=True,verbose_name='实例ID')
    assetGroupId = models.IntegerField(blank=True,verbose_name='主机组')
    resourceId = models.CharField(max_length=100, verbose_name='资源组ID')
    assetregionId = models.IntegerField(blank=True,verbose_name='region区域ID')
    securityGroupId = models.CharField(max_length=100, verbose_name='安全组ID')


# 资产表
class asset(models.Model):
    ostypechoice=(
        (0,'windows'),
        (1,'linux'),
        (2,'ubuntu'),
    )
    ecsnetwork = (
        (0,'classic'),
        (1,'vpc'),
    )
    chargetype = (
        (0,'PrePaid'),
        (1,'PostPaid'),
    )
    status_choice = (
        (0,'running'),
        (1,'starting'),
        (2,'stopping'),
        (3,'stopped')
    )
    instanceId = models.CharField(db_index=True,max_length=100,verbose_name='实例id')
    instanceName = models.CharField(max_length=200,verbose_name='实例名称')
    hostname = models.CharField(max_length=100, verbose_name='主机名')
    regionId = models.CharField(max_length=100,verbose_name='所属region')
    zoneId = models.CharField(max_length=100,verbose_name='所属可用区')
    instanceType = models.CharField(max_length=100,verbose_name='实例类型')
    keyPairName = models.CharField(blank=True,null=True,max_length=100,verbose_name='密钥对')
    status = models.IntegerField(choices=status_choice,blank=True,verbose_name='0-Running 1-Starting 2-Stopping 3-Stopped')
    tagKey = models.CharField(blank=True,null=True,max_length=100,verbose_name='标签key')
    tagValue = models.CharField(blank=True,null=True,max_length=100,verbose_name='标签value')
    instanceNetworkType = models.IntegerField(choices=ecsnetwork,verbose_name='实例网络类型 0-经典网络 1-vpc网络')
    instanceChargeType = models.IntegerField(choices=chargetype,verbose_name='付费类型 包年包月-PrePaid-0  按量付费-postpaid-1')
    osType = models.IntegerField(choices=ostypechoice,verbose_name='系统类型 0-windows 1-linux 2-ubuntu')
    osName = models.CharField(max_length=200,verbose_name='系统名称')
    cpu = models.IntegerField(verbose_name='cpu个数')
    memory = models.IntegerField(verbose_name='内存大小')
    ipType = models.IntegerField(verbose_name='ip类型 0-经典ip 1-弹性ip')
    publicIp = models.GenericIPAddressField(verbose_name='公网IP')
    privateIp = models.GenericIPAddressField(verbose_name='内网IP')
    createTime = models.DateTimeField(verbose_name='创建时间')
    expiredTime = models.DateTimeField(verbose_name='过期时间')


#弹性IP
class eip(models.Model):
    isp_choice=(
        (0,'BGP'),
        (1,'BGP_PRO'),
        (2,'no'),
    )
    eip_status = (
        (0, '未分配'),
        (1, '已分配'),
    )
    paytype =(
        (0,'PostPaid'),
        (1,'PrePaid'),
    )

    regionId = models.CharField(max_length=100, verbose_name='所属region')
    instanceId = models.CharField(max_length=100, verbose_name='所绑定实例ID')
    resourceId = models.CharField(max_length=100, verbose_name='所资源组ID')
    bandWidth = models.IntegerField(verbose_name="带宽峰值 ，单位是MBps")
    isp = models.IntegerField(choices=isp_choice,verbose_name="线路类型 0-BGP 1-BGP_PRO 2-")
    eipAdress = models.GenericIPAddressField(verbose_name="弹性IP地址")
    eipstatus = models.IntegerField(choices=eip_status,verbose_name="弹性IP状态 0-未分配 1-已分配") # 对应返回结果的Status字段 InUse
    chargeType=models.IntegerField(choices=paytype,verbose_name="付费方式 0-PostPaid 1-PrePaid")
    internetChargeType=models.IntegerField(verbose_name="弹性IP状态 0-PayByBandwidth 1-PayByTraffic")
    createTime = models.DateTimeField(verbose_name='创建时间')



#安全组
class securityGroup(models.Model):
    resourceId = models.CharField(max_length=100, verbose_name='资源组ID')
    securityGroupId = models.CharField(max_length=100, verbose_name='安全组ID')
    securityGroupType = models.IntegerField(verbose_name="安全组类型 0-normal 1-enterprise")
    vpcId = models.CharField(blank=True,null=True,max_length=100,verbose_name="所属vpc")
    networkType = models.IntegerField(verbose_name="如果vpc为空 则是经典网络 0-专有网络 1-经典网络")
    description = models.CharField(max_length=200,verbose_name="描述信息")
    createTime = models.DateTimeField(verbose_name='创建时间')


class securityGroupRule(models.Model):
    policychoice = (
        (0,"accept"),
        (1,"drop"),
    )
    securityGroupId = models.CharField(max_length=100, verbose_name='安全组ID')
    ipProtocol = models.IntegerField(verbose_name="传输层协议 0-tcp, 1-udp, 2-icmp, 3-all")
    portRange = models.CharField(max_length=20,verbose_name="端口范围 使用斜线（/）隔开起始端口和终止端口")
    policy  = models.IntegerField(default=0,choices=policychoice,verbose_name="0-accept,1-drop")
    priority = models.IntegerField(verbose_name="优先级1-100 1优先级最高")
    scrIp = models.CharField(max_length=50,verbose_name='允许访问的IP')
    description = models.CharField(max_length=200, verbose_name="描述信息")
    createTime = models.DateTimeField(verbose_name='创建时间')


#资源组
class resourceGroup(models.Model):
    name = models.CharField(max_length=300,verbose_name='资源组名称')
    accountId = models.IntegerField(verbose_name='所属账号ID')
    resourceId = models.CharField(max_length=100,verbose_name='资源组ID')
    status = models.CharField(max_length=100,verbose_name="资源组状态")
    displayName = models.CharField(null=True,blank=True,max_length=100,verbose_name='资源组显示名称')
    createTime = models.DateTimeField(verbose_name='创建时间')


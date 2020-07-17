from django.db import models
from django.db.backends.mysql.base import DatabaseWrapper
DatabaseWrapper.data_types = DatabaseWrapper._data_types

class projectinfo(models.Model):
    project = models.CharField(max_length=500,verbose_name='项目名称')
    project_type = models.CharField(max_length=200, verbose_name='项目类型')
    website_url = models.CharField(max_length=350, verbose_name='项目地址')
    gologin = models.BooleanField(verbose_name='是否可以登录')
    remarks = models.CharField(max_length=300, verbose_name='备注', null=True)

class projectName(models.Model):
    statusChoices=(
        (0, '停用'),
        (1, '正常'),
    )
    projectName = models.CharField(max_length=200, verbose_name='项目名称')
    projectHook = models.CharField(max_length=200, verbose_name='项目Hook')
    projectModel = models.CharField(max_length=500, verbose_name="项目模块")
    projectOwner = models.CharField(max_length=500, verbose_name="项目经理")
    projectLogo = models.CharField(max_length=500, verbose_name="项目logo地址")
    status = models.IntegerField(choices=statusChoices,verbose_name="使用状态")
    updateTime = models.DateTimeField(auto_now=True, verbose_name="更新时间")



#### 下面是资产列表相关
# 主机组
class hostGroup(models.Model):
    groupName = models.CharField(max_length=200,verbose_name='资产组')
    group = models.CharField(max_length=200,verbose_name='资产组')
    createTime = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

# 主机
class hostList(models.Model):
    instanceId = models.CharField(max_length=200,verbose_name='实例ID')
    InstanceName = models.CharField(blank=True, max_length=200,verbose_name='主机别名')
    osType = models.IntegerField(verbose_name='系统类型 0- linux 1- windows 2- ubuntu')
    ipAddress = models.CharField(blank=True,max_length=200,verbose_name='主机公网IP')
    status = models.CharField(max_length=100,verbose_name='实例状态')
    osName = models.CharField(max_length=100,verbose_name='系统类型')
    cpu = models.IntegerField(verbose_name='cpu数量')
    memory = models.IntegerField(verbose_name='内存大小')
    instanceNetworkType = models.IntegerField(verbose_name='网络类型 0-vpc网络 1-经典网络')
    instanceType = models.CharField(max_length=200, verbose_name='实例类型')
    createTime = models.DateTimeField(auto_now=True, verbose_name='创建时间')


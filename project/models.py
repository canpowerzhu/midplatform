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
    projectLogo = models.CharField(max_length=500, verbose_name="项目logo地址")
    status = models.IntegerField(choices=statusChoices,verbose_name="使用状态")
    updateTime = models.DateTimeField(auto_now=True, verbose_name="更新时间")
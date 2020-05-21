from django.db import models

# Create your models here.

class projectinfo(models.Model):
    project = models.CharField(max_length=500,verbose_name='项目名称')
    project_type = models.CharField(max_length=200, verbose_name='项目类型')
    website_url = models.CharField(max_length=350, verbose_name='项目地址')
    gologin = models.BooleanField(verbose_name='是否可以登录')
    remarks = models.CharField(max_length=300, verbose_name='备注', null=True)

class ProjectName(models.Model):
    projectName = models.CharField(max_length=200, verbose_name='项目名称')
    ProjectHook = models.CharField(max_length=200, verbose_name='项目Hook')
    ProjectModel = models.CharField(max_length=500, verbose_name="项目模块")
    ProjectLogo = models.CharField(max_length=500, verbose_name="项目logo地址")
    status = models.BooleanField(verbose_name="使用状态")
    UpdateTime = models.DateTimeField(auto_now=True, verbose_name="更新时间")
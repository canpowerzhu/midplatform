from django.db import models
from django.db.backends.mysql.base import DatabaseWrapper
DatabaseWrapper.data_types = DatabaseWrapper._data_types

# Create your models here.
class configinfo(models.Model):
    parentId = models.CharField(max_length=20,verbose_name='所属层级')
    versioncode = models.IntegerField(unique=True,verbose_name='配置版本号')
    versionname = models.CharField(max_length=20,verbose_name='配置版本名称')
    content = models.TextField(verbose_name='文件内容')
    iscurversion = models.BooleanField(default=False,verbose_name='是否是当前版本')
    author = models.CharField(max_length=200,verbose_name='创建者')
    lastauthor = models.CharField(max_length=200,verbose_name='最后一次修改者')
    description = models.CharField(null=True,blank=True,max_length=500,verbose_name='描述信息')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')



class configTree(models.Model):
    name = models.CharField(max_length=300,verbose_name='名称')
    parentId = models.IntegerField(verbose_name='父节点')
    hierarchy = models.CharField(max_length=30,verbose_name='层级关系')
    depth = models.IntegerField(verbose_name='深度')
    sort = models.IntegerField(verbose_name='排序值')
    author = models.CharField(max_length=200,verbose_name='创建者')
    description = models.CharField(null=True,blank=True,max_length=500,verbose_name='描述信息')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

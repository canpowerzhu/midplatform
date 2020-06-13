from django.db import models
# from django.contrib.postgres.fields import JSONField
import jsonfield
from django.db.backends.mysql.base import DatabaseWrapper
DatabaseWrapper.data_types = DatabaseWrapper._data_types



class taskList(models.Model):
    """
    监控任务列表
    """
    taskProject = models.CharField(max_length=500, verbose_name='监控任务所属项目')
    taskName = models.CharField(max_length=500, verbose_name='监控任务名称')
    taskUrl = models.CharField(max_length=500, verbose_name='监控任务地址')
    reqMethod = models.IntegerField(default=0,verbose_name='请求方式0-get 1-post')
    taskRate = models.IntegerField(verbose_name='执行频率 5，10, 30mins')
    taskStatus = models.IntegerField(default=0, verbose_name='任务状态 0-正常，1-警告，2-致命')
    alarmRule = models.IntegerField(verbose_name="0-不包含匹配内容报警 1-包含匹配内容报警")
    postBody =  models.CharField(max_length=500,blank=True,verbose_name='请求体内容')
    ruleContent = models.CharField(blank=True,max_length=500, verbose_name="规则内容")
    deleted = models.IntegerField(default=1, verbose_name='0 删除，1 正常')
    disabled = models.IntegerField(default=1, verbose_name='0 禁用，1 启用')
    createTime = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

class scanLog(models.Model):
    """
    监控日志
    """
    taskProject = models.CharField(max_length=500, verbose_name='监控任务所属项目')
    taskName = models.CharField(max_length=500, verbose_name='监控任务名称')


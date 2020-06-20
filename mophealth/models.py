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
    taskType = models.CharField(db_index=True, max_length=500, verbose_name='任务类型：0- 服务状态，1- 业务状态')
    reqMethod = models.IntegerField(default=0,verbose_name='请求方式0-get 1-post')
    taskRate = models.IntegerField(verbose_name='执行频率 5，10, 30mins')
    taskStatus = models.IntegerField(default=0, verbose_name='任务状态 0-正常，1-警告，2-致命')
    alarmRule = models.IntegerField(verbose_name="0-不包含匹配内容报警 1-包含匹配内容报警")
    reqBody =  models.CharField(max_length=500,blank=True,verbose_name='请求体内容')
    reqHeader =  models.CharField(max_length=500,blank=True,verbose_name='请求头内容')
    ruleContent = models.CharField(blank=True,max_length=500, verbose_name="规则内容")
    thresholdCount = models.IntegerField(default=3, verbose_name="连续几次超过阈值后报警")
    deleted = models.IntegerField(default=1, verbose_name='0 删除，1 正常')
    disabled = models.IntegerField(default=1, verbose_name='0 禁用，1 启用')
    createTime = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

class scanLog(models.Model):
    """
    监控日志
    """
    taskId = models.UUIDField(editable = False)
    taskProject = models.CharField(max_length=50, verbose_name='监控任务所属项目')
    taskName = models.CharField(max_length=50, verbose_name='监控任务名称')
    taskType = models.CharField(db_index=True, max_length=5, verbose_name='任务类型：0- 服务状态，1- 业务状态')
    responseTime = models.CharField(max_length=10, verbose_name='响应时间')
    preResult = models.CharField(max_length=20, verbose_name='上一次响应结果')
    curResult = models.CharField(max_length=20, verbose_name='当前响应结果')
    responseResult = models.CharField(max_length=20, verbose_name='响应结果')
    errorNum = models.CharField(max_length=10, verbose_name='异常次数 前端 不断更新')
    createTime = models.DateTimeField(auto_now=True, verbose_name='创建时间')


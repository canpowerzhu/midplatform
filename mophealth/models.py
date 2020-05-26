from django.db import models
# from django.contrib.postgres.fields import JSONField
import jsonfield
from django.db.backends.mysql.base import DatabaseWrapper
DatabaseWrapper.data_types = DatabaseWrapper._data_types



class Tasklist(models.Model):
    TYPE_CHOICES = (
        (0, 'get'),
        (1, 'post'),
    )
    STATUS_CHOICES = (
        (0, 'normal'),
        (1,'warnning'),
        (2, 'fatal')
    )
    taskproject = models.CharField(max_length=500, verbose_name='监控任务所属项目')
    taskname = models.CharField(max_length=500, verbose_name='监控任务名称')
    taskurl = models.CharField(max_length=500, verbose_name='监控任务名称')
    req_method = models.IntegerField(choices=TYPE_CHOICES, verbose_name='请求方式get/post')
    taskrate = models.IntegerField(verbose_name='执行频率 5，10, 30mins')
    taskstatus = models.IntegerField(choices=STATUS_CHOICES, verbose_name='任务状态 正常，异常，不可用')
    alarmrule = models.IntegerField(verbose_name="0-不包含匹配内容报警 1-包含匹配内容报警")
    postbody = jsonfield.JSONField()
    rulecontent = models.CharField(max_length=500, verbose_name="规则内容")
    del_flag = models.IntegerField(default=1, verbose_name='0 删除，1 正常')
    avaliable_flag = models.IntegerField(default=1, verbose_name='0 禁用，1 启用')
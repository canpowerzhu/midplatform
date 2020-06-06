from django.db import models
from django.db.backends.mysql.base import DatabaseWrapper
DatabaseWrapper.data_types = DatabaseWrapper._data_types
# Create your models here.
from django.db import models

# Create your models here.


class deployRecord(models.Model):
    stateChoice =(
        (0,'未处理'),
        (1,'失败'),
        (2,'成功'),
    )
    cacheChoice = (
        (0,'未修改'),
        (1,'修改'),
    )

    projectName = models.CharField(max_length=200, verbose_name="项目名称")
    isRollBack = models.BooleanField(verbose_name="是否可以回滚")
    modifyModel = models.CharField(max_length=1024, verbose_name="更新哪些模块")
    modifyContent = models.TextField(max_length=5120, verbose_name="更新的内容")
    state = models.IntegerField(choices=stateChoice,verbose_name="更新进度 0- 未处理，1- 失败， 2-成功")
    publisher = models.CharField(max_length=500, verbose_name="发布负责人")
    isModifyCache = models.IntegerField(default=0,choices=cacheChoice,verbose_name="是否修改缓存")
    cacheDetail = models.TextField(blank=True,max_length=1024, verbose_name="修改缓存详情")
    isModifySql = models.IntegerField(default=0,choices=cacheChoice,verbose_name="是否修改数据库")
    sqlDetail = models.TextField(blank=True,max_length=10240, verbose_name="修改数据库详情")
    deployTime = models.DateTimeField(auto_now_add=True, verbose_name="发布开始时间")
    finishTime = models.DateTimeField(blank=True,null=True,verbose_name="发布完成时间")
    elapsedTime = models.IntegerField(blank=True,null=True,verbose_name="发布耗时 单位为分钟")





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
    state = models.IntegerField(choices=stateChoice,verbose_name="更新进度 0- 未处理，1- 处理中，2-失败 ，3-成功")
    publisher = models.CharField(max_length=500, verbose_name="发布负责人")
    isModifyCache = models.IntegerField(default=0,choices=cacheChoice,verbose_name="是否修改缓存")
    cacheDetail = models.TextField(blank=True,max_length=1024, verbose_name="修改缓存详情")
    isModifySql = models.IntegerField(default=0,choices=cacheChoice,verbose_name="是否修改数据库")
    sqlDetail = models.TextField(blank=True,max_length=10240, verbose_name="修改数据库详情")
    tester = models.CharField(blank=True,max_length=200, verbose_name="测试人员")
    testStatus = models.CharField(blank=True, max_length=200, verbose_name="测试状态 0-测试失败 1-测试成功")
    testResult = models.CharField(blank=True,max_length=200, verbose_name="测试结论")
    aduitStatus = models.CharField(blank=True,max_length=200, verbose_name="审核状态 0-审核失败 1-审核成功")
    aduitResult = models.CharField(blank=True,max_length=200, verbose_name="审核拒绝的原因 项目经理填写")
    arrangeStatus = models.CharField(blank=True, max_length=200, verbose_name="部署状态 0-部署失败 1-部署成功")
    arrangeResult = models.CharField(blank=True, max_length=200, verbose_name="部署失败的原因 运维人员填写")
    deployStatus = models.CharField(blank=True, max_length=200, verbose_name="发布状态 0-发布失败 1-发布成功")
    deployResult = models.CharField(blank=True, max_length=200, verbose_name="发布失败原因 测试人员填写")
    step = models.IntegerField(default=1,verbose_name="发布进度 0-开发人员填写完成 1-测试人员填写 2-项目经理审核完成 3-部署完成 4-线上测试完成")
    deployTime = models.DateTimeField(auto_now_add=True, verbose_name="发布开始时间")
    finishTime = models.DateTimeField(blank=True,null=True,verbose_name="发布完成时间")
    elapsedTime = models.IntegerField(blank=True,null=True,verbose_name="发布耗时 单位为分钟")


class issueRecord(models.Model):
    recordId = models.IntegerField(verbose_name='关联发布记录的记录ID 可点击超链接查看详情')
    content = models.TextField(verbose_name='详细问题')
    srcIP = models.CharField(max_length=20, verbose_name='操作IP')
    username = models.CharField(max_length=20, verbose_name='哪位用户操作')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')


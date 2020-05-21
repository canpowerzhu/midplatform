from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class DeployRecord(models.Model):
    ProjectName = models.CharField(max_length=200, verbose_name="项目名称")
    isRollBack = models.BooleanField(verbose_name="是否可以回滚")
    ModifyModel = models.CharField(max_length=1024, verbose_name="更新哪些模块")
    ModifyContent = models.TextField(max_length=5120, verbose_name="更新的内容")
    state = models.IntegerField(verbose_name="更新进度 0- 未处理，1- 失败， 2-成功")
    Publisher = models.CharField(max_length=500, verbose_name="发布负责人")
    isModifyCache = models.BooleanField(verbose_name="是否修改缓存")
    CacheDetail = models.TextField(max_length=1024, verbose_name="修改缓存详情")
    isModifySql = models.BooleanField(verbose_name="是否修改数据库")
    SqlDetail = models.TextField(max_length=10240, verbose_name="修改数据库详情")
    DeployTime = models.DateTimeField(auto_now_add=True, verbose_name="发布开始时间")
    FinishTime = models.DateTimeField(blank=True,null=True,verbose_name="发布完成时间")
    ElapsedTime = models.IntegerField(blank=True,null=True,verbose_name="发布耗时 单位为分钟")





from django.db import models

from django.db.backends.mysql.base import DatabaseWrapper

DatabaseWrapper.data_types = DatabaseWrapper._data_types


#### apklist 模块
class apklist(models.Model):
    envTypeChoices = (
        (0,'正式环境'),
        (1,'测试环境'),
    )
    projectName = models.CharField(max_length=500, null=True, blank=True, verbose_name='项目名称')
    packageName = models.CharField(max_length=500, null=True, blank=True, verbose_name="apk包名")
    version = models.IntegerField( verbose_name='版本号')
    envType = models.IntegerField(choices=envTypeChoices,verbose_name='正式环境-0 测试环境-1')
    size = models.DecimalField(max_digits=5, decimal_places=2,verbose_name='apk文件大小， 单位为MB')
    owner = models.CharField(max_length=100, verbose_name='提交人')
    url = models.CharField(max_length=300, verbose_name='apk下载地址')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        unique_together = ('packageName', 'version','envType')

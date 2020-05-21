from django.db import models


#### apklist 模块
class apklist(models.Model):
    projectname = models.CharField(max_length=500, null=True, blank=True, verbose_name='项目名称')
    packagename = models.CharField(max_length=500, null=True, blank=True, verbose_name="apk包名")
    version = models.IntegerField( verbose_name='版本号')
    envtype = models.BooleanField(verbose_name='正式环境-0 测试环境-1')
    size = models.DecimalField(max_digits=5, decimal_places=2,verbose_name='apk文件大小， 单位为MB')
    owner = models.CharField(max_length=100, verbose_name='提交人')
    url = models.CharField(max_length=300, verbose_name='apk下载地址')
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        unique_together = ('packagename', 'version','envtype')

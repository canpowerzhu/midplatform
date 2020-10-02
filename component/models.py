from django.db import models

from django.db.backends.mysql.base import DatabaseWrapper

DatabaseWrapper.data_types = DatabaseWrapper._data_types


# apklist 模块
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





# loggger设计
class operatelog(models.Model):
    traceId = models.CharField(max_length=100,verbose_name='追踪ID 每个用户登陆到登出期间操作的日志 为同一个traceID')
    username = models.CharField(blank=True,null=True,max_length=300, verbose_name='操作的用户名')
    protocol = models.CharField(max_length=100,verbose_name='采用协议')
    path = models.CharField(max_length=500, verbose_name='请求路径')
    msg = models.CharField(max_length=500,verbose_name='日志消息 自定义写入')
    method = models.CharField(max_length=200, verbose_name='请求方式')
    ipAdress = models.GenericIPAddressField(verbose_name='请求IP地址')
    params = models.TextField(blank=True,null=True,verbose_name="请求参数")
    status = models.BooleanField(verbose_name='操作状态 0-异常 1-正常')
    operateType = models.CharField(max_length=500,verbose_name='操作类型 修改 新增 删除等')
    requestTime = models.DateTimeField(verbose_name='请求时间')


class login_out(models.Model):
    traceId = models.CharField(max_length=100,verbose_name='登陆时 产生一个traceId')
    username = models.CharField(max_length=100,verbose_name='用户名')
    status = models.BooleanField(verbose_name='登陆状态 0-失败 1-成功')
    osType = models.CharField(max_length=200, verbose_name='操作系统类型')
    broswerType = models.CharField(max_length=100, verbose_name='浏览器类型')
    broswerVersion = models.CharField(max_length=100, verbose_name='浏览器版本')
    userAgent = models.CharField(max_length=500, verbose_name='useragent信息')
    action = models.BooleanField(verbose_name='0-登出 1-登陆')
    requestTime = models.DateTimeField(verbose_name='请求时间')






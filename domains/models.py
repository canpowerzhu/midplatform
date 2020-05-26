from django.db import models
from django.db.backends.mysql.base import DatabaseWrapper
DatabaseWrapper.data_types = DatabaseWrapper._data_types
### 域名相关
class Domainaccount(models.Model):
    register_website = models.CharField(max_length=50, verbose_name="域名注册服务商")
    username = models.CharField(max_length=50, verbose_name="域名账户")
    password = models.CharField(max_length=50, verbose_name="域名账户密码")
    token_name = models.CharField(max_length=100, default='', verbose_name="令牌名称")
    token = models.CharField(max_length=100,default='', verbose_name="令牌")
    account_code = models.CharField(max_length=50, verbose_name="域名账户码")
    status = models.CharField(max_length=50, verbose_name="域名账户是否有域名 1 表示账户下有域名, 0 则没有域名")
    remark = models.CharField(max_length=100)

class Domaininfo(models.Model):
    project = models.CharField(max_length=100, verbose_name="项目名称")
    register_website = models.CharField(max_length=100)
    name_account = models.CharField(max_length=100, verbose_name="所属账户")
    domain_name = models.CharField(max_length=100, verbose_name="根域名")
    fqdn = models.CharField(max_length=100, verbose_name="二级域名")
    type = models.CharField(max_length=20, verbose_name="域名解析方式A、CNAME、TXT")
    answer = models.CharField(max_length=500, verbose_name="解析的属性值")
    remark = models.CharField(max_length=20, verbose_name="合作伙伴或者是域名用途")

class Domainlist(models.Model):
    name_account = models.CharField(max_length=100, verbose_name="所属账户")
    domainName = models.CharField(max_length=100, verbose_name="域名")
    locked = models.BooleanField(verbose_name="是否锁定")
    autorenewEnabled = models.BooleanField(verbose_name="是否自动续费")
    expireDate = models.DateField(verbose_name="过期时间")
    createDate = models.DateField(verbose_name="创建时间")
## 项目相关
class projectinfo(models.Model):
    project = models.CharField(max_length=500,verbose_name='项目名称')
    project_type = models.CharField(max_length=200, verbose_name='项目类型')
    website_url = models.CharField(max_length=350, verbose_name='项目地址')
    gologin = models.BooleanField(verbose_name='是否可以登录')
    remarks = models.CharField(max_length=300, verbose_name='备注', null=True)
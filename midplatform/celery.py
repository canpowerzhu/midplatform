from celery import Celery
from django.conf import  settings
import os

# 获取当前文件夹名，即为该Django的项目名
project_name = os.path.split(os.path.abspath('.'))[-1]
project_settings = '%s.settings' % project_name

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', project_settings)

# 实例化Celery,网上很多教程这里都是没有设置broker造成启动失败
app = Celery('tasks', broker='redis://192.168.1.5:8006/0')

# 使用django的settings文件配置celery
app.config_from_object('django.conf:settings')

# Celery加载所有注册的应用
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
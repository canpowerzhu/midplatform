# @Author  : kane.zhu
# @Time    : 2020/11/3 15:44
# @Software: PyCharm
from django.conf.urls import url
from ansibletower import views


urlpatterns = [
    url(r'^configlist/', views.configlist),

]

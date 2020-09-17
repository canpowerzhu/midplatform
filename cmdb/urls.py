# @Author  : kane.zhu
# @Time    : 2020/8/16 15:13
# @Software: PyCharm


from django.conf.urls import url
from cmdb import views



urlpatterns = [
    url(r'^region/', views.region),
    url(r'^assetgroup/', views.assetgroup),
    url(r'^asset/', views.asset),
    url(r'^eipinfo/', views.eipinfo),
    url(r'^resourceGroup/', views.resourceGroup),
    url(r'^syncbill/', views.syncbill),
]

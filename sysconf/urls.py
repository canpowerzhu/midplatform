from django.conf.urls import url
from sysconf import views



urlpatterns = [
    url(r'^router/', views.router),
    url(r'^changemailserver/', views.changemailserver),
    url(r'^ossconf/', views.ossconf),
    url(r'^modifyossconf/', views.modifyossconf),
    url(r'^mailserver/', views.mailserver),
    url(r'^getrouter/', views.getrouter),
    # url(r'^editrouter/', views.editrouter),
    # url(r'^deleterouter/', views.deleterouter),
    # url(r'^listrouter/', views.listrouter),
]


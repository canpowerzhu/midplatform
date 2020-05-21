from django.conf.urls import url
from project import views



urlpatterns = [
    url(r'^urlinfo/', views.urlinfo),
    url(r'^addurlinfo/', views.addurlinfo),
    url(r'^urlinfoselect/', views.urlinfoselect),
    url(r'^editlogin/', views.editlogin),
    url(r'^getbaseinfo/', views.getbaseinfo),
    url(r'^addbaseinfo/', views.addbaseinfo),
    url(r'^modifybaseinfo$', views.modifybaseinfo),

    url(r'^getproname/', views.getproname),
    url(r'^getmodelname/', views.getmodelname),
]

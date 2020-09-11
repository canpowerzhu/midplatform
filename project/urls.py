from django.conf.urls import url
from project import views



urlpatterns = [
    url(r'^urlinfo/', views.urlinfo),
    url(r'^urlinfoselect/', views.urlinfoselect),
    url(r'^baseinfo/', views.baseinfo),
    url(r'^getproname/', views.getproname),
    url(r'^getmodelname/', views.getmodelname),
]

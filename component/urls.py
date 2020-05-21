from django.conf.urls import url
from component import views



urlpatterns = [
    url(r'^getapklist/', views.getapklist),
    url(r'^upload/', views.upload),

]

from mophealth import views
from django.conf.urls import url




urlpatterns = [
    url(r'^tasklist/', views.tasklist),
    url(r'^taskStatus/', views.taskStatus),

]

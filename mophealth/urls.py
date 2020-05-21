from mophealth import views
from django.conf.urls import url




urlpatterns = [
    url(r'^addtask/', views.addtask),
    url(r'^gettask/', views.gettask),
    url(r'^edittask/', views.edittask),
]

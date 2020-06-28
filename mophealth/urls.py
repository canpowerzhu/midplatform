from mophealth import views
from django.conf.urls import url




urlpatterns = [
    url(r'^tasklist/', views.tasklist),
    url(r'^test/', views.test),
    url(r'^test2/', views.test2),

]

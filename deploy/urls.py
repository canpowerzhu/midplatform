from django.conf.urls import url
from deploy import views


urlpatterns = [
    url(r'^addrecord/', views.addrecord),
    url(r'^editrecord/', views.editrecord),
    url(r'^getallrecord/', views.getallrecord),
    url(r'^dingrecord/', views.dingrecord),
    url(r'^issuerecord/', views.issuerecord),
    url(r'^issuerecordpic/', views.issuerecordpic),
    url(r'^getrecordanalyse/', views.getrecordanalyse),
]

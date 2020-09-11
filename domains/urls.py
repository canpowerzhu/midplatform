from django.conf.urls import url
from domains import views



urlpatterns = [
    url(r'^accountlist/', views.accountlist),
    url(r'^domaininfo/', views.domaininfo),
    url(r'^domainsync/', views.domainsync),
    url(r'^recordinfo/', views.recordinfo),
    # 这个$ 是为了修改任何不匹配或尾部没有斜杠(/)的申请URL，将被重定向至尾部包含斜杠的相同字眼的URL。
    url(r'^modifydomianinfo/', views.modifydomianinfo),
    url(r'^domainlist/', views.domainlist),
    url(r'^modifyaccount/', views.modifyaccount),

]

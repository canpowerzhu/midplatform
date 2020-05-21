
from django.conf.urls import url, include
from django.contrib import admin
from .views import  login,home


urlpatterns = [
    url(r'^admin/doc/',include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^domains/', include("domains.urls")),
    url(r'^component/', include("component.urls")),
    url(r'^deploy/', include("deploy.urls")),
    url(r'^sysconf/', include("sysconf.urls")),
    url(r'^project/', include("project.urls")),
    url(r'^mophealth/', include("mophealth.urls")),
]

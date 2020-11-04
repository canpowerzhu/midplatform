
from django.conf.urls import url, include
from django.contrib import admin





urlpatterns = [
    url(r'^/',include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^domains/', include("domains.urls")),
    url(r'^component/', include("component.urls")),
    url(r'^deploy/', include("deploy.urls")),
    url(r'^sysconf/', include("sysconf.urls")),
    url(r'^project/', include("project.urls")),
    url(r'^mophealth/', include("mophealth.urls")),
    url(r'^cmdb/', include("cmdb.urls")),
    url(r'^ansibletower/', include("ansibletower.urls")),

]

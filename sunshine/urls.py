from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import Home


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^', include('library.urls')),
    url(r'^', include('spine.urls')),
    url(r'^', include('sajax.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

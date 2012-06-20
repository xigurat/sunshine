

from django.conf.urls.defaults import patterns, url
from .views import Books


urlpatterns = patterns('',
    url(r'^$', Books.as_view(),
        name='library_books'),
    url(r'^user/(?P<username>\w+)/(?P<catalog_path>[/\w]+)$', Books.as_view(),
        name='library_user_books'),
    url(r'^book/(?P<id>\d+)/$', Books.as_view(),
        name='library_book_details'),
)

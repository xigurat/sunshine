

from django.conf.urls.defaults import patterns, url
from .views import BookUpload, BookEdit, BookDetails, MyBooks, UserBooks


urlpatterns = patterns('',
    url(r'^$', BookUpload.as_view(),
        name='library_book_upload'),
    url(r'^mybooks/$', MyBooks.as_view(),
        name='library_my_books'),
    url(r'^userbooks/$', UserBooks.as_view(),
        name='library_user_books'),
    url(r'^document/(?P<id>\d+)/$', BookDetails.as_view(),
        name='library_book_details'),
    url(r'^docuemnt/(?P<id>\d+)/edit/$', BookEdit.as_view(),
        name='library_book_edit'),
)

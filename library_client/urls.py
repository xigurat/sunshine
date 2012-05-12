

from django.conf.urls.defaults import patterns, url
from .views import BookUpload, BookEdit, BookDetails, MyBooks, UserBooks


urlpatterns = patterns('',
    url(r'^book/upload/$', BookUpload.as_view(),
        name='library_book_upload'),
    url(r'^book/mybooks/$', MyBooks.as_view(),
        name='library_my_books'),
    url(r'^book/userbooks/$', UserBooks.as_view(),
        name='library_user_books'),
    url(r'^book/(?P<id>\d+)/$', BookDetails.as_view(),
        name='library_book_details'),
    url(r'^book/(?P<id>\d+)/edit/$', BookEdit.as_view(),
        name='library_book_edit'),
)

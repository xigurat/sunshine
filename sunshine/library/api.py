

from spine.api import SpineAPI
#from django.utils.decorators import method_decorator
#from django.contrib.auth.decorators import login_required
#from piston.utils import rc, throttle

from .models import Author, Book
from .forms import BookForm, BookUploadForm


class AuthorHandler(SpineAPI):
    model = Author
    page_size = 10
    http_method_names = ('get', 'post')


class BookHandler(SpineAPI):
    model = Book
    page_size = 10
    add_form_class = BookUploadForm
    edit_form_class = BookForm
    serialize_fields = (
        'id', 'title', 'title', 'n_pages', 'date', 'authors', 'summary',
        'date', 'uploader_username', 'upload_datetime', 'file',
        'thumbnail_url', 'short_url',

        #ajax file upload flag
        'success',
    )

    def serialize(self, data):
        success = self.request.method == 'POST' and isinstance(data, Book)
        if isinstance(data, dict):
            data['success'] = success
        else:
            data.success = success
        return super(BookHandler, self).serialize(data)

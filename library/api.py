

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
        'title', 'language', 'id', 'summary', 'n_pages', 'get_absolute_url',
        'short_url', 'date', 'uploader_username', 'thumbnail_url', 'file',
        'get_edition_url', 'later_editions_ids',
        'previous_editions_ids', 'success',

        #DC fields
        'source', 'relation', 'format',

        #ajax file upload flag
        'success',
    )

    def serialize(self, data):
        data.success = self.request.method == 'POST' and isinstance(data, Book)
        return super(BookHandler, self).serialize(data)

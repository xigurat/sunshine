# Create your views here.


from django.http import HttpResponseRedirect
from django.utils import simplejson as json
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from .forms import BookUploadForm, BookForm
from .models import Book


class BookUpload(TemplateView):
    template_name = 'library/book_upload.html'

    def get_context_data(self, book_upload_form=None):
        """
        Returns the view context

        book_upload_form: the form instance.
        book: is returned if the book uploaded is duplicated
                and is the duplicated uploaded before.
        """
        context = super(BookUpload, self).get_context_data()
        book_upload_form = book_upload_form or BookUploadForm()

        #if 'file' in book_upload_form.errors:
        #    try:
        #        equal_mongo_file = book_upload_form.mongo_file_nonrel.equals[0]
        #        context['book'] = equal_mongo_file.mongo_file.book_file
        #    except (IndexError, MongoFile.DoesNotExist) as e:
        #        pass

        context['book_upload_form'] = book_upload_form
        return context

    def post(self, request, *args, **kwargs):
        book_upload_form = BookUploadForm(request.POST, request.FILES)
        if book_upload_form.is_valid():
            book = book_upload_form.save()
            return HttpResponseRedirect(book.get_edition_url())
        else:
            return self.get(self, request, book_upload_form=book_upload_form,
                                *args, **kwargs)


class BookDetails(TemplateView):
    template_name = 'library/book_details.html'

    def get_context_data(self, *args, **kwargs):
        book = get_object_or_404(Book, **kwargs)
        context = super(BookDetails, self).get_context_data()
        context['book'] = book
        return context

class MyBooks(TemplateView):
    template_name = 'library/my_books.html'

class UserBooks(TemplateView):
    template_name = 'library/user_books.html'


class BookEdit(BookDetails):
    template_name = 'library/book_edit.html'

    def get_context_data(self, *args, **kwargs):
        context = super(BookEdit, self).get_context_data(*args, **kwargs)
        context['book_form'] = BookForm(instance=context['book'])
        return context




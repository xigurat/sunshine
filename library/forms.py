
from os.path import splitext, basename
from mimetypes import guess_type

from django import forms
from django.utils.translation import ugettext as _

from .models import Book
from .settings import Settings as settings
from .offline import post_process


class BookUploadForm(forms.ModelForm):
    FILE_NAME_SEPARATOR = '._-'

    class Meta:
        model = Book
        fields = ('file',)

    file = forms.FileField(
            widget=forms.ClearableFileInput(attrs={'multiple': 'multiple'}))

    def clean_file(self):
        mimetype = guess_type(self.cleaned_data['file'].name)
        if mimetype not in settings.LIBRARY_ALLOWED_BOOK_TYPES:
            raise forms.ValidationError(_('Sorry, the file type is incorrect'))
        return self.cleaned_data['file']

    def save(self):
        book = super(BookUploadForm, self).save(commit=False)
        book.calculate_file_hash()
        duplicate = book.duplicate

        if duplicate:
            return duplicate
        else:
            book.title = get_title(book.file.name)
            book.save()
            post_process(book.id)
            return book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'summary')


#TODO: Test this
def uncammel_case(file_name):
    title = []
    is_last_lower = False
    for c in file_name:
        c_is_upper = c.isupper()
        if c != '0' and c_is_upper and is_last_lower:
            title.append(' ')
        title.append(c)
        is_last_lower = not c_is_upper
    return ''.join(title).strip()


#TODO: Test this
def get_title(file_name, file_name_separators=r'[\._-]'):
    file_name, extension = splitext(basename(file_name))
    for separator in file_name_separators:
        file_name = file_name.replace(separator, ' ')
    return uncammel_case(file_name)

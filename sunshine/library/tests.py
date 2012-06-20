
from os.path import abspath, dirname, join

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from .models import Book


class UploadBookTest(TestCase):
    TEST_FILES_PATH = join(dirname(abspath(__file__)), 'test_files')
    PDF_FILE_PATH = join(TEST_FILES_PATH, 'tema1.pdf')
    NON_PDF_FILE_PATH = join(TEST_FILES_PATH, 'icono.png')

    def setUp(self):
        self.client = Client()
        #ensure that there are not repeated books
        self._upload(file=open(self.PDF_FILE_PATH))
        self.tearDown()

    def tearDown(self):
        for instance in Book.objects.all():
            if instance.file: instance.file.delete()
            if instance.thumbnail: instance.thumbnail.delete()

    def _upload(self, **kwargs):
        response = self.client.post(reverse('library_book_upload'), kwargs)
        self.assertTrue(response.status_code in (200, 302))
        return response

    def test_success_upload(self):
        response = self._upload(file=open(self.PDF_FILE_PATH))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.all().count(), 1)
        return Book.objects.all()[0]

    def test_upload_wrong_file(self):
        response = self._upload(file=open(self.NON_PDF_FILE_PATH))
        self.assertTrue('book' not in response.context)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['book_upload_form'].errors), 1)
        self.assertTrue('file' in response.context['book_upload_form'].errors)

    def test_upload_duplicated_books(self):
        book1 = self.test_success_upload()
        book2 = self.test_success_upload()
        self.assertEqual(book1, book2)


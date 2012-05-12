
import os
from os.path import join
from hashlib import sha256
from mimetypes import guess_type

import Image

from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.core.files import File
from django.utils.translation import ugettext_lazy as _

from short import short
#~ import object_permissions

from .managers import AuthorManager
from .commands import pdf2png, get_pdf_info
from .settings import Settings as settings
from .signals import book_post_processed


BLANK_PREVIEW = 'library/images/blank-preview.png'

def resource(url):
    domain = Site.objects.get_current().domain
    return 'http://{0}{1}'.format(domain, url)


class BookEncryptedError(Exception):
    pass


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, db_index=True)

    objects = AuthorManager()

    def __unicode__(self):
        return self.name


class Book(models.Model):

    class Meta:
        verbose_name = _('book')
        verbose_name_plural = _('books')
        ordering = ('-date',)

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name=_('title'))
    n_pages = models.IntegerField(default=0)
    date = models.DateTimeField(null=True, blank=True, db_index=True)
    language = models.CharField(max_length=4, default=u'none')
    authors = models.ManyToManyField(Author, null=True, blank=True)
    summary = models.TextField(blank=True, null=True)
    is_indexed = models.BooleanField(default=False, db_index=True)

    uploader_username = models.CharField(max_length=30, db_index=True)
    upload_datetime = models.DateTimeField(auto_now_add=True)
    indexed_datetime = models.DateTimeField(null=True)

    file = models.FileField(upload_to='book/%Y/%m/%d', max_length=1024)
    file_sha256 = models.CharField(max_length=64, db_index=True)
    thumbnail = models.ImageField(upload_to='thumbnail/%Y/%m/%d', null=True)

    _previous_edition = models.ForeignKey('self', null=True)

    _short_url = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return u'%s - %s' % (self.id, self.title)

    def calculate_file_hash(self):
        hash = sha256()
        for chunk in self.file.chunks():
            hash.update(chunk)
        self.file_sha256 = hash.hexdigest()

    # extended properties

    @property
    def uploader(self):
        try:
            return User.objects.get(username=self.uploader_username)
        except User.DoesNotExist:
            return None

    @uploader.setter
    def uploader(self, user):
        self.uploader_usernanme = user.username

    # relation helpers

    @property
    def previous_edition(self):
        return self._previous_edition

    @previous_edition.setter
    def previous_edition(self, other):
        """
        Algorithm:
            precondition: I am newest than the other book
            If I have no an older edition then:
                the other book is my older one
            else:
                if the other book is newest than my previous edition then:
                    it is in the middle: me -> other -> me._previous_edition
                else: (if it is older)
                    it is the previous edition of my previous edition
        """
        #TODO: estan ocurriendo relaciones recursivas..
        assert self != other
        assert self.date > other.date, '%s - %s' % (self.date, other.date)
        if self._previous_edition is None:
            self._previous_edition = other
        else:
            if self._previous_edition.date < other.date:
                other._previous_edition = self._previous_edition
                self._previous_edition = other
            else:
                self._previous_edition.previous_edition = other
        self.save()

    @property
    def duplicate(self):
        for book in type(self).objects.filter(file_sha256=self.file_sha256):
            if book.id != self.id:
                return book
        return None

    @property
    def later_editions(self):
        return type(self).objects.filter(_previous_edition=self)

    @property
    def later_editions_ids(self):
        return [(book.id, book.title) for book in self.later_editions]

    @property
    def previous_editions(self):
        book = self
        while book._previous_edition:
            yield book._previous_edition
            book = book._previous_edition

    @property
    def previous_editions_ids(self):
        return [(book.id, book.title) for book in self.previous_editions]

    # URLs

    @property
    def thumbnail_url(self,
        generic_url=join(settings.STATIC_URL, BLANK_PREVIEW)):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            return generic_url

    @property
    def short_url(self):
        if not self._short_url:
            self._short_url = short(self.relation)
            self.save()
        return self._short_url

    @models.permalink
    def get_absolute_url(self):
        return 'library_book_details', (), {'id': self.id}

    @models.permalink
    def get_edition_url(self):
        return 'library_book_edit', (), {'id': self.id}


    # DublinCore Interface

    @property
    def source(self):
        return resource(self.file.url)

    @property
    def relation(self):
        return resource(self.get_absolute_url())

    @property
    def creator(self):
        return self.authors.all()

    @property
    def format(self):
        return guess_type(self.file.name)[0]

    # Tasks

    def post_process(self):
        pdf_info = self._get_info()
        self.date = pdf_info.last_modification
        self.n_pages = pdf_info.n_pages
        self.save()
        self.thumbnail, old_image = self._generate_thumbnail()
        self.save()
        os.remove(old_image)
        book_post_processed.send(Book, book=self)

    def _get_info(self):
        info = get_pdf_info(self.file.path)
        if info.is_encrypted:
            self.delete()
            raise BookEncryptedError(self.id)
        return info

    def _generate_thumbnail(self):
        assert self.n_pages, self.n_pages
        img_file_path = pdf2png(self.file.path, last=1)[1]
        thumbnail = Image.open(img_file_path)
        thumbnail.thumbnail(
            (settings.LIBRARY_BOOK_THUMBNAIL_WIDTH,
             settings.LIBRARY_BOOK_THUMBNAIL_HEIGHT),
             resample=Image.ANTIALIAS,
        )
        thumbnail.save(img_file_path)
        return File(open(img_file_path)), img_file_path


class Catalog(models.Model):
    class Meta:
        verbose_name = _("Catalog")
        verbose_name_plural = _("Catalogs")

    parent = models.ForeignKey('self', null=True)
    name = models.CharField(max_length=64)
    owner = models.ForeignKey(User)
    books = models.ManyToManyField(Book)
    is_public = models.BooleanField(default=True)

    @property
    def childs(self):
        return type(self).objects.filter(parent=self)

    def get_childs(self, **kwargs):
        return type(self).objects.filter(parent=self, **kwargs)


#~ CATALOG_PERMS = {
    #~ 'perms' : {
        #~ # perm with both params
        #~ 'can_delete': {
            #~ 'description':'Can delete a catalog',
            #~ 'label':'Perm One'
        #~ },
    #~ },
    #~ #'url':'test_model-detail',
    #~ #'url-params':['name']
#~ }
#~
#~ object_permissions.register(CATALOG_PERMS, Catalog, 'library')

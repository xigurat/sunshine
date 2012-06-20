
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Author, Book
from .offline import post_process


class BookAdmin(admin.ModelAdmin):
    actions = ['make_post_processing']

    def make_post_processing(self, request, queryset):
        for book in queryset:
            post_process(book.id)
        self.message_user(
            request,
            _('Started postproccessing of %s books.') % queryset.count())

    make_post_processing.short_description = _(
        'Extracts metadata and preview image from books, then index them'
    )


admin.site.register(Author)
admin.site.register(Book, BookAdmin)


from django.conf import settings


def SettingsResolver(name, bases, attrs):
    for name, value in attrs.iteritems():
        if not '__' in name:
            attrs[name] = getattr(settings, name, value)
    return type(name, bases, attrs)


class Settings(object):
    __metaclass__ = SettingsResolver

    STATIC_URL = None
    LIBRARY_ALLOWED_BOOK_TYPES = (('application/pdf', None),)
    LIBRARY_BOOK_THUMBNAIL_WIDTH = 128
    LIBRARY_BOOK_THUMBNAIL_HEIGHT = 163



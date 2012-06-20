

from django.conf.urls import patterns
from django.conf import settings
from django.utils.importlib import import_module

from .utils import get_sajax_functions, get_url


callback_urls = []


for app_name in settings.INSTALLED_APPS:
    try:
        module = import_module('%s.ajax' % app_name)
    except ImportError as e:
        if str(e) != 'No module named ajax':
            print '>>> Error in %s.ajax, %s !!!' % (app_name, e)
    else:
        for sajax_function in get_sajax_functions(module):
            callback_urls.append(get_url(sajax_function))


urlpatterns = patterns('', *callback_urls)

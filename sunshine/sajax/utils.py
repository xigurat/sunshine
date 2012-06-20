
from django.conf.urls import url


def get_sajax_functions(module):
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if callable(attr) and hasattr(attr, '__sajax__'):
            yield attr


def get_url(sajax_function, prefix='sajax'):
    app_label = sajax_function.__module__.split('.')[-2]
    name = sajax_function.__name__
    my_url = r'^%s/%s/%s/$' % (prefix, app_label, name)
    return url(my_url, sajax_function)

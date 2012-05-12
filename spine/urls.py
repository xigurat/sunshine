#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       urls.py
#
#       Copyright 2012 Eddy Ernesto del Valle Pino <edelvalle@hab.uci.cu>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#
#


from django.conf import settings
from django.conf.urls.defaults import patterns
from django.utils.importlib import import_module

from .utils import get_api_classes
from .api import api_handlers


api_urls = []


for api_handler in api_handlers.itervalues():
    api_urls.extend(api_handler.get_urls())


for app_name in settings.INSTALLED_APPS:
    try:
        api_module = import_module('%s.api' % app_name)
    except ImportError:
        pass
    else:
        for api_class in get_api_classes(api_module):
            api_urls.extend(api_class.get_urls())


urlpatterns = patterns('', *api_urls)

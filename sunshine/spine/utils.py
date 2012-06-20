#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       utils.py
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


import sys


def get_app_label(any_thing):
    """
    If any thing is not a class it is converted to its type
    Resolves the application label of the class
    If the class is a Model this function can get better results
    """
    klass = any_thing if isinstance(any_thing, type) else type(any_thing)
    if hasattr(klass, '_meta') and hasattr(klass._meta, 'app_label'):
        app_label = klass._meta.app_label
    else:
        model_module = sys.modules[klass.__module__]
        app_label = model_module.__name__.split('.')[-2]
    return app_label


def flatten_dict(dct):
    """
    Converts a MultiDict into a dict
    """
    return {str(k): dct.get(k) for k in dct.keys()}


def object_to_dict(obj, attrs):
    """
    Converts a object to a dict using the attrs parameter, if the attribute is
    not found is not returnedn in the dict
    """
    return {attr: getattr(obj, attr) for attr in attrs if hasattr(obj, attr)}


def get_field_names(model):
    """
    Returns all the field names of a model
    """
    return [f.name for f in model._meta.fields] if model else []


def get_api_classes(api_module):
    """
    Given a module returns all the SpineAPI subclasses that
    has a model deffined
    """
    from .api import SpineAPI
    for attr_name in dir(api_module):
        attr = getattr(api_module, attr_name)
        if (isinstance(attr, type)
            and attr is not SpineAPI
            and issubclass(attr, SpineAPI)
            and attr.get_model_name()):
            yield attr

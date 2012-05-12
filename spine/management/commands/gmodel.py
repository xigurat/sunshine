#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       gmodel.py
#
#       Copyright 2012 Eddy Ernesto del Valle Pino <edelvalle@hab.uci.cu>
#       Copyright 2012 Leiser Fernández Gallo <lfgallo@estudiantes.uci.cu>
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

import os

from django.core.management.base import BaseCommand
from django.utils.importlib import import_module
from django.template import Context, loader
from django.conf import settings

from ...utils import get_api_classes


class Command(BaseCommand):
    args = '<AppName AppName...>'
    help = 'Create Spine Models.'
    spine_model_template_name = 'spine/model.coffee'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.spine_model_template = loader.get_template(
                self.spine_model_template_name)

    # commands interface

    def handle(self, *args, **options):
        for app in args:
            if app in settings.INSTALLED_APPS:
                self.stdout.write('Generating models for %s:\n' % app)
                self.generate_spine_models(app)
            else:
                self.stderr.write('%s is not an instaled application!' % app)

    # models generation

    def generate_spine_models(self, app_name):
        app = import_module(app_name)
        try:
            api_module = import_module('%s.api' % app_name)
        except ImportError:
            msg = 'The module %s.api not exist or has an error\n'
            self.stderr.write(msg % app_name)
        else:
            context = get_context(api_module)
            for api in context['apis']:
                self.stdout.write(' - %s\n' % api['name'])
            context['app_name'] = app_name
            context['name_space'] = underscored_to_CammelCase(app_name)
            self.write_spine_model_file(app, app_name, Context(context))

    def write_spine_model_file(self, app, app_name, context):
        app_path = os.path.abspath(os.path.dirname(app.__file__))
        spine_models_dir = os.path.join(app_path, 'static', app_name)
        try:
            os.makedirs(spine_models_dir)
        except OSError:
            pass

        spine_model_path = os.path.join(spine_models_dir, 'models.coffee')
        with open(spine_model_path, 'w') as spine_model_file:
            output = self.spine_model_template.render(context)
            spine_model_file.write(output)

        os.system('coffee -c %s' % spine_model_path)


# SpineAPI introspection

def get_context(api_module):
    """
    Generates the context for all SpineAPI subtypes in the api_module
    """
    apis = []
    for api_class in get_api_classes(api_module):
        api_context = {
            'name': api_class.get_model_name(),
            'fields': api_class.get_serialize_fields(),
        }
        apis.append(api_context)
    return {'apis': apis}


# string utils


def underscored_to_CammelCase(string):
    """
    Transforms 'app_name' -> 'AppName'
    """
    return string.replace('_', ' ').title().replace(' ', '')

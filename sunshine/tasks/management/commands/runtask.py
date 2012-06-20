#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       sin título.py
#
#       Copyright 2011 E E del Valle <edelvalle@uci.cu>
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

import sys

from django.core.management.base import BaseCommand
from ...models import Task


class Command(BaseCommand):
    help = 'Task processor daemon'
    
    requires_model_validation = True
    can_import_settings = True
    
    def handle(self, taskid, *args, **options):
        try:
            task = Task.objects.get(pk=int(taskid))
        except Task.DoesNotExist:
            sys.exit(2)
        else:
            task.start()


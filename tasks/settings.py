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

from multiprocessing import cpu_count
from django.conf import settings


def SettingsResolver(name, bases, attrs):
    for name, value in attrs.iteritems():
        if not '__' in name:
            attrs[name] = getattr(settings, name, value)
    return type(name, bases, attrs)


class Settings(object):
    __metaclass__ = SettingsResolver

    PROJECT_PATH = None
    TASKS_EXPIRED_CHEKING_TICKS = 60
    TASKS_CHECKING_INTERVAL = 1
    TASKS_MAX_IN_EXECUTION = cpu_count()
    TASKS_SCHEDULER_DATA_PATH = '/tmp/'
    TASKS_SCHEDULER_PIDFILE = 'tasks_scheduler.pid'
    TASKS_SCHEDULER_STDOUT = 'tasks_scheduler_stdout.txt'
    TASKS_SCHEDULER_STDERR = 'tasks_scheduler_stderr.txt'
    TASKS_TASK_PIDFILE = 'task_%s.pid'

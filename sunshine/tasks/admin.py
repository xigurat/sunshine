#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       admin.py
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

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import Task, TaskError


class TaskAdmin(admin.ModelAdmin):
    """Represents the model Task in the Django Admin interface"""

    list_display = (
        'function_name', 'args', 'kwargs', 'is_runing', 'is_enabled',
        'created', 'last_try',
    )

    actions = ('make_retry',)

    def make_retry(self, request, queryset):
        for task in queryset:
            task.retry()
    make_retry.short_description = _('Retry tasks')


class TaskErrorAdmin(admin.ModelAdmin):
    list_display = ('task', 'is_critical', 'date')
    list_filter = ('is_critical',)

    actions = ('make_retry',)

    def make_retry(self, request, queryset):
        """Retries disabled tasks
        @param request: django request
        @param queryset: selected pastes
        """
        for task_error in queryset:
            if not task_error.task.is_enabled:
                task_error.retry()
    make_retry.short_description = _('Retry tasks')


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskError, TaskErrorAdmin)

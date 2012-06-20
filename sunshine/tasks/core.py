#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       core.py
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

import time
from os import makedirs
from os.path import join, exists

from .settings import Settings as settings
from .daemon import Daemon
from .models import Task


class TaskScheduler(Daemon):
    """
    This is the task scheduler
    It will check if there are task unexecuted and will take some of them to
    execute it
    """

    def __init__(self):
        path = settings.TASKS_SCHEDULER_DATA_PATH
        if not(exists(path)):
            makedirs(path)

        super(TaskScheduler, self).__init__(
              pidfile=join(path, settings.TASKS_SCHEDULER_PIDFILE),
              std_out=join(path, settings.TASKS_SCHEDULER_STDOUT),
              std_err=join(path, settings.TASKS_SCHEDULER_STDERR))

    def run(self):
        """
        Algorithm:
          If there were tasks runing here all them will be tried latter,
            because they were interrupted.
          ticks = 0
          In an infinite loop:
            run unexecuted tasks
            increment a tick
            if is time:
              check for expired tasks
              ticks = 0
            wait
        """
        Task.objects.retry_all_executing_here()
        n_ticks = 0
        while True:
            self._run_tasks()
            n_ticks += 1
            if n_ticks == settings.TASKS_EXPIRED_CHEKING_TICKS:
                self._check_expired_tasks()
                n_ticks = 0
            time.sleep(settings.TASKS_CHECKING_INTERVAL)

    def _run_tasks(self):
        """
        While there are free workers:
          take some task and execute it and adds it to _in_execution_here
        """
        n_in_execution_here = Task.objects.in_execution_here.count()
        n_free_workers = settings.TASKS_MAX_IN_EXECUTION - n_in_execution_here
        while n_free_workers:
            task = Task.objects.one_todo
            if task:
                task.start(daemonize=False)
            n_free_workers -= 1

    def _check_expired_tasks(self):
        """
        If there are alive expired tasks retry them
        """
        for task in Task.objects.in_execution_here:
            if task and task.has_expired:
                task.retry()

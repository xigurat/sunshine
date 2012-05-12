#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from socket import gethostname

from django.db import models


class TaskManager(models.Manager):

    @property
    def in_execution_here(self):
        return self.filter(
                is_enabled=True, is_runing=True, running_in_host=gethostname())

    def retry_all_executing_here(self):
        for task in self.in_execution_here:
            task.retry()

    @property
    def one_todo(self):
        for task in self.filter(is_enabled=True, is_runing=False):
            return task

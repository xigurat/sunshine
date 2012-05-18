#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import os
import traceback
from socket import gethostname
from os.path import join
from datetime import datetime
from thread import start_new_thread

import django.utils.simplejson as json
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .settings import Settings as settings
from .daemon import Daemon
from .managers import TaskManager


class Task(models.Model, Daemon):
    function_name = models.TextField()
    module_name = models.TextField()
    args = models.TextField()
    kwargs = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    last_try = models.DateTimeField(auto_now=True, db_index=True)
    is_runing = models.BooleanField(default=False, db_index=True)
    running_in_host = models.CharField(
            max_length=128, db_index=True, null=True, blank=True)
    is_enabled = models.BooleanField(default=True, db_index=True)
    runing_since = models.DateTimeField(null=True)

    class Meta:
        ordering = ['last_try']
        verbose_name = _('task')
        verbose_name_plural = _('tasks')

    objects = TaskManager()

    def __init__(self, *args, **kw):
        self._encode_kwargs('args', kw)
        self._encode_kwargs('kwargs', kw)
        super(Task, self).__init__(*args, **kw)
        path = settings.TASKS_SCHEDULER_DATA_PATH
        Daemon.__init__(self, settings.TASKS_TASK_PIDFILE % self.id,
          std_out=join(path, settings.TASKS_SCHEDULER_STDOUT),
          std_err=join(path, settings.TASKS_SCHEDULER_STDERR))
        self._function = None

    def __unicode__(self):
        result = u'%s.%s args: %s, kw: %s' % (
          self.module_name, self.function_name, self.args, self.kwargs)
        return result

    @property
    def function(self):
        """Returns the function to execute"""
        if self._function is None:
            self._function = dynamic_import(
                    self.module_name, self.function_name)
        return self._function

    @property
    def is_runing_here(self):
        result = (
            self.is_runing
            and self.is_enabled
            and self.running_in_host == gethostname()
        )
        return result

    @property
    def has_expired(self):
        if self.is_runing_here and self.function.expiration_time:
            delta = self.function.expiration_time
            expected_finalization = datetime.now() - delta
            return expected_finalization > self.runing_since
        else:
            return False

    def start(self, daemonize=True):
        if daemonize:
            Daemon.start(self)
            self.log('Started')
        else:
            self.log('Sended to be executed')
            self.is_runing = True
            self.runing_since = datetime.now()
            self.running_in_host = gethostname()
            self.save()
            os.chdir(settings.PROJECT_PATH)
            start_new_thread(
                os.system,
                ('python manage.py runtask ' + str(self.id),))

    def run(self):
        """
        Runs the task
        - if an expected exception occurs the task y tried later
        - if an unexpected exceptions occurs the task is deleted
        - if the tasks runs successfully it is deleted
        """
        try:
            self.log('Runing')
            args, kwargs = self._decode(self.args), self._decode(self.kwargs)
            self.function(__EXECUTE_IT__=True, *args, **kwargs)
            self.log('Ended')
            self.delete()
        except self.function.exceptions as ex:
            self._report_error(ex)
            self.log('Expected error: %s' % ex)
            self.retry()
        except self.function.ignore as ex:
            self.log('Ignoring erorr: %s' % ex)
            self.delete()
        except BaseException as ex:
            self._report_error(ex, is_critical=True)
            self.log('Critical error %s' % ex)
            self.is_enabled = False
            self.save()
        finally:
            sys.stdout.flush()
            sys.stderr.flush()

    def _report_error(self, exception, is_critical=False):
        TaskError(
            task=self,
            is_critical=is_critical,
            traceback=unicode(traceback.format_exc()),
            exception=unicode(type(exception))).save()

    def retry(self):
        """Retries the task if it is alive the runing task is terminated."""
        self.log('Retring')
        self.is_runing = False
        self.is_enabled = True
        self.save()
        self.taskerror_set.all().delete()
        self.stop()

    def log(self, text):
        Daemon.log(self, '>>> TASK %s: %s' % (self.id, text))

    @classmethod
    def _encode_kwargs(cls, key, kwargs):
        """Encodes the arguments to json"""
        if key in kwargs and not isinstance(kwargs[key], basestring):
            kwargs[key] = cls._encode(kwargs[key])

    _encode = staticmethod(lambda data: json.dumps(data))
    _decode = staticmethod(lambda json_data: json.loads(json_data))


class TaskError(models.Model):

    task = models.ForeignKey(Task)
    traceback = models.TextField()
    exception = models.TextField()
    is_critical = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = _('task error')
        verbose_name_plural = _('task errors')

    def __unicode__(self):
        return unicode(self.task)

    def retry(self):
        self.task.retry()


def dynamic_import(module_name, member_name):
    module_name = str(module_name)
    member_name = str(member_name)
    module = __import__(module_name, fromlist=[member_name])
    member = getattr(module, member_name)
    return member

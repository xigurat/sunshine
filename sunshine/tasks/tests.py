"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from os import remove
from os.path import abspath, dirname, join, exists
from datetime import datetime, timedelta

from django.test import TestCase

from .decorators import task
from .models import Task, TaskError


_TEST_FILE = join(dirname(abspath(__file__)), 'test.txt')

@task()
def _test_task():
    test_file = open(_TEST_FILE, 'w')
    test_file.write('hi')
    test_file.close()


@task()
def _test_task_error():
    wa

class TestApp(TestCase):

    def setUp(self):
        self.n_tasks = Task.objects.count()
        self.task = _test_task()
        self.task_to_fail = _test_task_error()
        self.task.silent = True
        self.task_to_fail.silent = True
    
    def tearDown(self):
        if exists(_TEST_FILE):
            remove(_TEST_FILE)
    
        try:
            self.task.delete()
        except AssertionError:
            pass
        
        try:
            self.task_to_fail.delete()
        except AssertionError:
            pass
    
    def test_task_adition(self):
        self.assertEqual(Task.objects.count(), self.n_tasks + 2)
    
    def test_function_import(self):
        self.assertEqual(self.task.function, _test_task)
        self.assertEqual(self.task_to_fail.function, _test_task_error)
    
    def test_expiration_time(self):
        self.assertEqual(self.task.has_expired, False)
        self.assertEqual(self.task_to_fail.has_expired, False)
    
    def test_task_execution_send(self):
        self.task.start(daemonize=False)
        self.task = Task.objects.get(pk=self.task.id)
        self.assertTrue(self.task.is_runing)
        self.assertTrue(self.task.is_runing_here)
        delta_runing = datetime.now() - self.task.runing_since
        self.assertTrue(delta_runing < timedelta(seconds=5))
    
    def test_task_execution_successful(self):
        self.task.run()
        self.assertTrue(exists(_TEST_FILE))
        self.assertTrue(not Task.objects.filter(pk=self.task.id))
    
    def test_task_execution_error(self):
        self.task_to_fail.run()
        self.assertTrue(Task.objects.filter(pk=self.task_to_fail.id))
        self.assertTrue(TaskError.objects.filter(task=self.task_to_fail))




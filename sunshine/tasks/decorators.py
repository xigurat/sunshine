
from functools import wraps
from datetime import timedelta
from .models import Task

#TODO: test and document ignore parameter


def task(retry_if=None, expiration_time=None, ignore=None):
    """
    Task decorator
    @param retry_if Exceptions list, if one of this occurs the task will be
        retried latter.
    @param expiration_time datetime.deltatime if the task is un execution for
        more time than the expecified it will be retried latter.
    @param ignore exceptions to be ignore and give e normal finalization
        to the task
    """
    def decorator(function):
        function.exceptions = tuple(retry_if or [])
        function.ignore = tuple(ignore or [])
        function.expiration_time = expiration_time or timedelta(seconds=3600)

        @wraps(function)
        def wrapper(*args, **kw):
            if '__EXECUTE_IT__' in kw:
                del kw['__EXECUTE_IT__']
                return function(*args, **kw)
            else:
                task = Task(
                    function_name=function.__name__,
                    module_name=function.__module__,
                    args=args,
                    kwargs=kw)
                task.save()
                return task

        return wrapper
    return decorator

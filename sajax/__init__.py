

import json
from functools import wraps
from django.http import HttpResponse

try:
    from spine.api import SpineJSONEncoder
except ImportError:
    encode = json.dumps
else:
    encode = SpineJSONEncoder().encode


def register(function):
    @wraps(function)
    def wrapper(request):
        if request.method != 'POST':
            return HttpResponse(function.__doc__, mimetype='text/plain')

        response = function(request, **json.loads(request.body))
        return HttpResponse(encode(response), mimetype='application/json')
    wrapper.__sajax__ = True
    return wrapper

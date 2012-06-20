

import json
from functools import wraps

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import ugettext as _

try:
    from spine.api import SpineJSONEncoder
except ImportError:
    encode = json.dumps
else:
    encode = SpineJSONEncoder().encode


def register(function):
    @csrf_protect
    @wraps(function)
    def wrapper(request):
        if request.method != 'POST':
            response = HttpResponse(
                function.__doc__ or _('Undocumented'),
                mimetype='text/plain')
            return response

        response = function(request, **json.loads(request.body))
        return HttpResponse(encode(response), mimetype='application/json')
    wrapper.__sajax__ = True
    return wrapper

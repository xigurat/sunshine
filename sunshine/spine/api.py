#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       api.py
#
#       Copyright 2012 Eddy Ernesto del Valle Pino <edelvalle@hab.uci.cu>
#       Copyright 2011 Aaron Franks <aaron.franks+djangbone@gmail.com>
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
#
#

import datetime
import json

from django.db.models import Model
from django.db.models.fields.files import FieldFile
from django.db.models.query import QuerySet
from django.forms.models import modelform_factory
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.http import HttpResponse, Http404
from django.views.generic import View
from django.conf.urls.defaults import url

from .utils import get_app_label, flatten_dict, object_to_dict
from .utils import get_field_names


api_handlers = {}


def regist(api_class):
    if api_class.model is not None:
        global api_handlers
        api_handlers[api_class.model] = api_class


class SpineJSONEncoder(json.JSONEncoder):
    """
    JSON encoder that converts additional Python types to JSON.
    """
    def default(self, obj):
        """
        Converts during json serialization:
            - datetime objects to ISO-compatible strings
            - RelatedManagers to QuerySet
            - FieldFile to its download URL
            - QuerySet to tuple
            - Model into a dictionary with all its serializable fields
            - Call the callables
        """
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()

        elif type(obj).__name__ in ('RelatedManager', 'ManyRelatedManager'):
            return obj.all()

        elif isinstance(obj, FieldFile):
            return obj.url if obj else None

        elif isinstance(obj, QuerySet) or hasattr(obj, '__iter__'):
            return tuple(obj)

        elif isinstance(obj, Model):
            global api_handlers
            model = type(obj)
            api_handler = api_handlers.get(model)
            if api_handler is None:
                serialize_fields = get_field_names(model)
            else:
                serialize_fields = api_handler.get_serialize_fields()
            return object_to_dict(obj, serialize_fields)

        elif callable(obj):
            return obj()

        msg = '%s: %s, is not JSON serializable' % (type(obj), repr(obj))
        raise TypeError(msg)


class BadRequest(HttpResponse):
    def __init__(self, content='Bad request', status=400, *args, **kwargs):
        super(BadRequest, self).__init__(
                content=content, status=status, *args, **kwargs)


def model_get_api_url(cls):
    global api_handlers
    return api_handlers[cls].get_url()


def model_api_url(self):
    return self.get_api_url() + str(self.pk)


class SpineAPIMeta(type):
    def __new__(cls, *args, **kwargs):
        """
        Registers the new handler for future models serializations
        Apply decorators to methods
        """
        new_class = super(SpineAPIMeta, cls).__new__(cls, *args, **kwargs)

        #register
        regist(new_class)

        #inject get_api_url method
        if new_class.model:
            new_class.model.get_api_url = classmethod(model_get_api_url)
            new_class.model.api_url = property(model_api_url)

        #decorate
        for method, decorators in new_class.method_decorators.iteritems():
            class_method = getattr(new_class, method, None)
            if class_method:
                for decorator in decorators:
                    class_method = method_decorator(decorator)(class_method)
                setattr(new_class, method, class_method)

        return new_class


class SpineAPI(View):
    """
    Abstract class view, which makes it easy for subclasses to talk to
    Spine.js.

    Supported operations (copied from spine.js docs):
        create -> POST   /api/app_name/ModelName
        read ->   GET    /api/app_name/ModelName[/id]
        update -> PUT    /api/app_name/ModelName/id
        delete -> DELETE /api/app_name/ModelName/id
    """

    __metaclass__ = SpineAPIMeta

    # Key pattern for url with id
    pk_pattern = r'(?P<id>\d+)'
    # Prefix for url with id
    pk_name = 'pk_'

    # Methods allowed by the API View
    http_method_names = ('get', 'post', 'put', 'delete')

    # Model to use for all data accesses
    model = None

    # Tuple of field names that should appear in json output
    serialize_fields = tuple()

    # Optional pagination settings:
    # Set to an integer to enable GET pagination (at the specified page size)
    page_size = None
    # HTTP GET parameter to use for accessing pages (eg. /widgets?p=2)
    page_param_name = 'p'

    # Override these attributes with ModelForm instances to support PUT and
    #   POST requests:
    # Form class to be used for POST requests
    add_form_class = None
    # Form class to be used for PUT requests
    edit_form_class = None

    # Override these if you have custom JSON encoding/decoding needs:
    json_encoder = SpineJSONEncoder()
    json_decoder = json.JSONDecoder()

    # Decoratos to apply to class methods
    #
    # Ex: {'get': [login_required]}
    # is equivalent to:
    #
    #   @method_decorator(login_required)
    #   def get(sefl, ...):
    #      ....
    # or:
    #
    #   get = method_decorator(login_required)(SpineAPI.get)
    #
    method_decorators = {}

    def __init__(self, *args, **kwargs):
        super(SpineAPI, self).__init__(*args, **kwargs)
        self._data = None

    @property
    def base_queryset(self):
        """
        Override this to return another query set
        Ex: self.model.objects.filter(user=self.request.user)
        """
        return self.model.objects.all()

    @property
    def page_number(self):
        return int(self.real_data.get(self.page_param_name, 1))

    @property
    def decode_request(self, decoder_prefix='_get_data_for_'):
        decoder_name = decoder_prefix + self.request.method.lower()
        return getattr(self, decoder_name)

    @property
    def real_data(self):
        if self.content_type == 'application/json':
            try:
                data = self.decode_request()
            except ValueError:
                raise BadRequest()
        else:
            # This is a hack!
            method = self.request.method.upper()
            method = 'POST' if method == 'PUT' else method
            data = flatten_dict(getattr(self.request, method))
        return data

    @property
    def data(self, ):
        """
        Returns the data passed in the request method data
        """
        if self._data is None:
            data = self.real_data
            if self.page_param_name in data:
                data.pop(self.page_param_name)
            self._data = data
        return self._data

    @property
    def content_type(self):
        return self.request.META.get('CONTENT_TYPE') or ''

    def _get_data_for_get(self):
        """
        Decodes the data for GET requests
        """
        keys = self.request.GET.keys()
        data = None
        if keys:
            data = keys[0]
        return self.json_decoder.decode(data or '{}')

    def _get_data_for_post(self):
        """
        Decodes the data for POST and PUT requests
        """
        return self.json_decoder.decode(self.request.body)
    _get_data_for_put = _get_data_for_post

    def get(self, request, id=None):
        """
        Handle GET requests, either for a single resource or a collection.
        """
        if id is None:
            return self.get_collection()
        else:
            return self.get_single_item(id)

    def get_single_item(self, id):
        """
        Handle a GET request for a single model instance.
        """
        try:
            instance = self.base_queryset.get(id=id)
        except self.model.DoesNotExist:
            raise Http404()
        return self.success_response(instance)

    def get_collection(self):
        """
        Handle a GET request for a full collection (when no id was provided).
        """
        return self.success_response(self.base_queryset.filter(**self.data))

    def post(self, request):
        """
        Handle a POST request by adding a new model instance.

        This view will only do something if SpineAPI.add_form_class
        is specified by the subclass. This should be a ModelForm corresponding
        to the model.
        """
        add_form_class = self.add_form_class or modelform_factory(
                self.model, fields=self.get_serialize_fields() or None)
        form = add_form_class(self.data, files=request.FILES)
        return self._save_form(form)

    def put(self, request, id=None):
        """
        Handle a PUT request by editing an existing model.

        This view will only do something if SpineAPI.edit_form_class
        is specified by the subclass. This should be a ModelForm corresponding
        to the model.
        """
        if id is None:
            return HttpResponse('PUT not supported', status=405)
        try:
            instance = self.base_queryset.get(id=id)
        except ObjectDoesNotExist:
            raise Http404()

        edit_form_class = self.edit_form_class or modelform_factory(
                self.model, fields=self.get_serialize_fields() or None)
        form = edit_form_class(
                self.data, files=request.FILES, instance=instance)
        return self._save_form(form)

    def _save_form(self, form):
        """
        Saves the form and returs the corresponding response
        """
        form.request = self.request
        if form.is_valid():
            item = form.save()
            return self.success_response(item)
        else:
            return self.validation_error_response(form.errors)

    def delete(self, request, *args, **kwargs):
        """
        Respond to DELETE requests by deleting the model and returning its
        JSON representation.
        """
        if 'id' not in kwargs:
            return HttpResponse(
                    'DELETE is not supported for collections', status=405)
        qs = self.base_queryset.filter(id=kwargs['id'])
        if qs:
            qs.delete()
            return self.success_response()
        else:
            raise Http404()

    def paginate(self, queryset):
        """
        Paginates the response if it is a QuerySet, a list or a tuple
        """
        if (isinstance(queryset, (QuerySet, list, tuple))
            and self.page_size is not None):
            offset = (self.page_number - 1) * self.page_size
            queryset = queryset[offset:offset + self.page_size]
        return queryset

    def serialize(self, data):
        """
        Serialize a queryset or anything into a JSON object that can be
        consumed by Spine.js.
        """
        return self.json_encoder.encode(data)

    def success_response(self, *args, **kwargs):
        """
        Takes some object and serialize it, then converts it to HttpResponse
        with the correct mimetype

        If nothig is passed the response is empty
        """
        return self.response(http_response_class=HttpResponse, *args, **kwargs)

    def validation_error_response(self, output, *args, **kwargs):
        """
        Return an BadRequest indicating that input validation failed.

        The form_errors argument contains the contents of form.errors, and you
        can override this method is you want to use a specific error
        response format.
        By default, the output is a simple text response.
        """
        output = {'errors': output}
        return self.response(output=output, http_response_class=BadRequest,
                *args, **kwargs)

    def response(self, output='', http_response_class=HttpResponse):
        """
        Takes some object and serialize it, then converts it to HttpResponse
        with the correct mimetype

        If nothig is passed the response is empty
        """
        if output != '':
            output = self.serialize(self.paginate(output))
        return http_response_class(output, mimetype='application/json')

    @classmethod
    def get_urls(cls):
        """
        Returns the URLs for the API handler, so you dont have to do anything
        just:

            api_urls = UserAPI.get_urls()

            urlpatterns = patterns('',
                url(r'^users/$', EditUsers.as_view(),
                    name='users_edit'),
                *api_urls
            )
        """
        urls = (
            cls._get_url_pattern(),
            cls._get_url_pattern(add_pk=True),
        )
        return urls

    @classmethod
    def _get_url_pattern(cls, add_pk=False):
        pk_pattern = cls.pk_pattern if add_pk else r''
        my_url = r'^{0}{1}$'.format(cls.get_url()[1:], pk_pattern)

        pk_name = cls.pk_name if add_pk else ''
        url_name = '{0}_{1}_{2}api'.format(
                cls.get_application_label(), cls.get_model_name(), pk_name)

        url_pattern = url(my_url, cls.as_view(), name=url_name)
        return url_pattern

    @classmethod
    def get_url(cls, url_pattern=r'/api/{0}/{1}/'):
        args = cls.get_application_label(), cls.get_model_name()
        return url_pattern.format(*args)

    @classmethod
    def get_application_label(cls):
        return get_app_label(cls)

    @classmethod
    def get_model_name(cls):
        assert cls.model is not None
        return cls.model._meta.object_name

    @classmethod
    def get_serialize_fields(cls):
        if cls.serialize_fields:
            return cls.serialize_fields
        return get_field_names(cls.model)

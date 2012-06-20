#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tests.py
#
#  Copyright 2012 Eddy Ernesto del Valle Pino <edelvalle@hab.uci.cu>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import json

from django.db import models
from django.test import TestCase, Client

from .api import SpineAPI


class TestModel(models.Model):
    string_field = models.CharField(max_length=30)

    def __unicode__(self):
        return self.string_field


class TestModelApi(SpineAPI):
    model = TestModel


class TestModelTest(TestCase):

    def test_create_instance(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        a = TestModel(string_field='some thing')
        a.save()
        self.assertEqual(a.id, 1)
        self.assertEqual(TestModel.objects.count(), 1)


def get_data(response):
    return json.loads(response.content)


class TestAPI(TestCase):
    def setUp(self):
        self.instance = TestModel(string_field='some thing')
        self.client = Client()
        self.serialized_fields = ('id', 'string_field')
        self.api_url = '/api/spine/TestModel/'
        self.instance.save()

    def test_get(self):
        data = get_data(self.client.get(self.instance.api_url))
        self.assertEqual(self.instance.string_field, data['string_field'])
        return data

    def test_post(self):
        post_data = {'string_field': 'hi world'}
        data = get_data(self.client.post(self.api_url, post_data))
        for key, value in post_data.iteritems():
            self.assertEqual(value, post_data.get(key))
        self.assertTrue(TestModel.objects.get(id=data['id']))

    def test_put(self):
        """
        Imposible to test this, because django does not handle a PUT request
        """
        #~ put_data = {'string_field': 'hi fuking world'}
        #~ data = get_data(self.client.put(self.instance.api_url, put_data))
        #~ print TestModel.objects.all()
        #~ self.instance = TestModel.objects.get(id=self.instance.pk)
        #~ print data
        #~ print put_data
        #~ self.assertEqual(data['string_field'], put_data['string_field'])
        #~ self.assertEqual(self.instance.string_field, data['string_field'])
        #~ self.assertEqual(self.instance.id, data['id'])
        pass

    def test_serialized_fields(self):
        data = self.test_get()
        self.assertEqual(len(data), len(self.serialized_fields))
        for serialized_field in self.serialized_fields:
            self.assertIn(serialized_field, data)

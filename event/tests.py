# -*- coding: utf-8 -*-
import unittest

from werkzeug import Request, MultiDict

from kay.tests import TestCase

class UtilsTestCase(unittest.TestCase):
  import views

  def test_get_query_strings(self):
    self.assertEqual(self.views.get_query_strings(Request.from_values(query_string="")), MultiDict([]))
    self.assertEqual(self.views.get_query_strings(Request.from_values(query_string="test=1&TEST=2&test=3")), MultiDict([("test", "1"), ("TEST", "2"), ("test", "3")]))

class RESTTestCase(TestCase):

  def test_get_model(self):
    response = self.client.get('/event')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")

    response = self.client.get('/event.yaml')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")

    response = self.client.get('/event.json')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.headers["Content-Type"], "text/json; charset=utf-8")

    response = self.client.get('/event.UNKOWN')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")

  def test_get_item(self):
    response = self.client.get('/event/0')
    self.assertEqual(response.status_code, 404)
    self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")

    #response = self.client.get('/event/1')
    #self.assertEqual(response.status_code, 200)
    #self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")

  def test_head(self):
    response = self.client.head('/event')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")
    self.assertEqual("".join(response.response), "")

  def test_post_model(self):
    #ASYNC
    response = self.client.post('/event')
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")

    #SYNC
    response = self.client.post('/event?sync=true')
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")

    response = self.client.post('/event')
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")


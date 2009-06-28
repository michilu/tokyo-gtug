# -*- coding: utf-8 -*-
from kay.tests import TestCase

class RESTTestCase(TestCase):

  def test_get(self):
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

  def test_head(self):
    response = self.client.head('/event')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")
    self.assertEqual("".join(response.response), "")


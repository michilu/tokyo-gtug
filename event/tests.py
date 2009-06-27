# -*- coding: utf-8 -*-
from kay.tests import TestCase

class RESTTestCase(TestCase):

  def test_get(self):
    response = self.client.get('/event')
    self.failUnless(response.status_code == 200)

  def test_head(self):
    response = self.client.get('/event')
    self.failUnless(response.status_code == 200)

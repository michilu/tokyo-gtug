# -*- coding: utf-8 -*-
import unittest

from werkzeug import Client, BaseResponse, test_app

class BaseTestCase(unittest.TestCase):

  def setUp(self):
    pass

  def tearDown(self):
    pass

class RESTTestCase(BaseTestCase):

  def test(self):
    c = Client(test_app, BaseResponse)
    response = c.get('/')
    self.failUnless(response.status_code == 200)
    self.failUnless(response.status_code == 404)

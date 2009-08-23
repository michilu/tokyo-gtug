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
  def setUp(self):
    super(RESTTestCase, self).setUp()
    import event.models
    [m.delete() for m in event.models.Event.all().fetch(1000)]

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

  def test_get_model_index(self):
    import yaml
    response = self.client.get('/event?type=index')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")
    response_index = yaml.load("".join(response.response))
    self.assertEqual(response_index.keys(), ["index"])
    self.assertTrue(all(isinstance(i, int) for i in response_index["index"]))

  def test_get_item(self):
    data = "DATA"

    #SetUp
    response = self.client.post('/event?sync=true', data={"data": data})
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")
    self.assertNotEqual("".join(response.response), "")

    #Test
    response = self.client.get('/event/0')
    self.assertEqual(response.status_code, 404)
    self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")

    response = self.client.get('/event/1')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")

    response = self.client.get('/event/1.json')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.headers["Content-Type"], "text/json; charset=utf-8")

    response = self.client.get('/event/10000000000000')
    self.assertEqual(response.status_code, 404)
    self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")

  def test_get_slice(self):
    #response = self.client.get('/event/1:2')
    #response = self.client.get('/event/-2:-2')
    pass

  def test_head(self):
    response = self.client.head('/event')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")
    self.assertEqual("".join(response.response), "")

  def test_async_post_model(self):
    from StringIO import StringIO

    data = "DATA"

    response = self.client.post('/event')
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")

    response = self.client.post('/event.json')
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.headers["Content-Type"], "text/json; charset=utf-8")

    self.assertRaises(AssertionError, self.client.post, '/event', data={"data": data})
    self.assertRaises(AssertionError, self.client.post, '/event', data={"file": (StringIO(data), "data.txt")})
    return
    response = self.client.post('/event', data={"data": data})
    self.assertEqual(response.status_code, 202)
    self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")
    #self.assertEqual(response.headers["Location"], "/queue?$unixtime:$nodeid")

    response = self.client.post('/event', data={"file": (StringIO(data), "data.txt")})
    self.assertEqual(response.status_code, 202)
    self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")
    #self.assertEqual(response.headers["Location"], "/queue?$unixtime:$nodeid")

  def test_sync_post_model(self):
    from StringIO import StringIO

    import yaml

    data = "DATA"

    def test(length=0):
      response = self.client.get('/event')
      self.assertEqual(response.status_code, 200)
      self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")
      content = yaml.load("".join(response.response))
      self.assertEqual(len(content["data"]), length)

    test(0)

    response = self.client.post('/event?sync=true')
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")

    test(0)

    response = self.client.post('/event?sync=true', data={"data": data})
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")
    #self.assertEqual(response.headers["Location"], "/event/$id")
    self.assertNotEqual("".join(response.response), "")

    test(1)

    response = self.client.post('/event?sync=true', data={"file": (StringIO(data), "data.txt")})
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")
    #self.assertEqual(response.headers["Location"], "/event/$id")
    self.assertNotEqual("".join(response.response), "")

    test(2)

  def test_sync_put_model(self):
    from StringIO import StringIO

    import yaml

    data = "DATA"

    def test(id=0, status_code=None):
      default = 200
      if status_code == None:
        status_code = default
      response = self.client.get('/event/%s' % id)
      self.assertEqual(response.status_code, status_code)
      self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")
      if status_code != default:
        return
      content = yaml.load("".join(response.response))
      self.assertEqual(len(content["data"]), 1)

    test(0, 404)

    response = self.client.put('/event/0?sync=true', data={"data": data})
    self.assertEqual(response.status_code, 400)

    test(0, 404)
    test("ITEM", 404)

    response = self.client.put('/event/ITEM?sync=true', data={"data": data})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")
    self.assertNotEqual("".join(response.response), "")

    test("ITEM")

    response = self.client.put('/event/ITEM?sync=true', data={"data": data})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.headers["Content-Type"], "text/yaml; charset=utf-8")
    self.assertNotEqual("".join(response.response), "")

    test("ITEM")


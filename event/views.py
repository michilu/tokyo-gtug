# -*- coding: utf-8 -*-
import logging

from google.appengine.api import memcache, users
from google.appengine.api.labs import taskqueue
from google.appengine.ext import db
from werkzeug import (
  unescape, redirect, Response, MultiDict
)
from werkzeug.exceptions import (
  HTTPException,
  NotFound, MethodNotAllowed, BadRequest
)
from werkzeug._internal import HTTP_STATUS_CODES
from kay.utils import (
  render_to_response, reverse,
  get_by_key_name_or_404, get_by_id_or_404,
  to_utc, to_local_timezone, url_for, raise_on_dev
)
from kay.i18n import gettext as _
from kay.auth.decorators import login_required

def get_query_strings(request):
  return MultiDict((q.split("=") for q in request.environ["QUERY_STRING"].split("&") if "=" in q))

def get(request, model, item):
  #data = model.get_by_key_name(item)
  #return 200, dict(data=data), {}
  #--
  if item == None:
    data = model.all().fetch(100)
  elif isinstance(item, int):
    try:
      data = model.get_by_id(item)
    except db.BadKeyError:
      raise NotFound
    else:
      if data:
        data = [data]
      else:
        raise NotFound
  else:
    try:
      data = model.get_by_key_name(item)
    except db.BadArgumentError:
      raise NotFound
    else:
      if data:
        data = data.get()
      else:
        raise NotFound
  return 200, dict(data=data), {}

def head(request, model, item):
  return get(request, model, item)

def is_sync(data):
  if isinstance(data, dict):
    return data.get("sync") == True
  elif isinstance(data, basestring):
    return

def post(request, model, item):
  if item != None:
    raise
  import yaml
  raw = request.form
  if not raw:
    raise BadRequest
  data = yaml.load(raw.keys()[0])
  if isinstance(data, dict):
    if data.get("sync") != True:
     if get_query_strings(request).get("sync") != "true":
       _data, _mimetype = format_yaml({"sync": True, "request": request})
       task = taskqueue.add(url=request.environ["PATH_INFO"], payload=_data)
       all = model.all().fetch(100)
       result = {"data":data, "all":all, "count":len(all), "task": task}
       return 202, result, {}
    _request = data.get("request")
  else:
    if get_query_strings(request).get("sync") != "true":
      _data, _mimetype = format_yaml({"sync": True, "request": request})
      task = taskqueue.add(url=request.environ["PATH_INFO"], payload=_data)
      all = model.all().fetch(100)
      result = {"data":data, "all":all, "count":len(all), "task": task}
      return 202, result, {}
    _request = data
  data = model(**(dict((x,x) for x in ["comment", "title", "start", "discription"])))
  __request, _mimetype = format_yaml(request)
  data.discription = _request or __request
  data.put()
  return 201, data, {}

def put(request, model, item):
  return 200, dict(data=request.environ["REQUEST_METHOD"]), {}

def delete(request, model, item):
  return 200, dict(data=request.environ["REQUEST_METHOD"]), {}

def options(request, model, item):
  return 200, dict(data=request.environ["REQUEST_METHOD"]), {}

def trace(request, model, item):
  return 200, dict(data=request.environ["REQUEST_METHOD"]), {}

class Methods(dict):
  def __getitem__(self, name):
    def func(*argv, **kwargv):
      try:
        return super(Methods, self).__getitem__(name)(*argv, **kwargv)
      except HTTPException, e:
        import re
        return e.code, dict(
          status_code = e.code,
          errors = [HTTP_STATUS_CODES[e.code], re.sub(r"<(/)?p>", "", e.description)],
        ), {}
    return func

methods = Methods({
  "GET": get,
  "HEAD": head,
  "POST": post,
  "PUT": put,
  "DELETE": delete,
  "OPTIONS": options,
  "TRACE": trace,
})

def format_json(data):
  import simplejson as json
  result = list()
  if "data" in data.keys():
    for d in data["data"]:
      item = dict()
      item.update(d._entity)
      item.update(id=d.key().id())
      item.update(key=str(d.key()))
      result.append(item)
  else:
    result = data
  return json.dumps(result, indent=2, skipkeys=True), "text/json"

def format_yaml(data):
  import yaml
  return yaml.dump(data, default_flow_style=False), "text/yaml"

def format_xml(data):
  data = [d.to_xml() for d in data["data"]]
  return data, "text/xml"

class Formater(dict):
  def __getitem__(self, name):
    try:
      return super(Formater, self).__getitem__(name)
    except KeyError:
      return super(Formater, self).__getitem__("yaml")

formater = Formater({
  "json": format_json,
  "yaml": format_yaml,
})

def rest(model, methods=methods, acl=None, formater=formater):
  def func(request, item=None, format="yaml"):
    method = request.environ["REQUEST_METHOD"]
    if method in methods:
      status_code, data, headers = methods[method](request, model, item)
      result, mimetype = formater[format](data)
    else:
      raise
    return Response(_(result if result.endswith("\n") else "%s\n" % result),
             status=status_code, headers=headers, mimetype=mimetype)
  return func

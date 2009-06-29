# -*- coding: utf-8 -*-
import logging

from google.appengine.api import memcache, users
from google.appengine.ext import db
from werkzeug import (
  unescape, redirect, Response,
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

def get(request, model, item):
  if item == None:
    data = model.all()
  elif isinstance(item, int):
    try:
      data = model.get_by_id(item)
    except db.BadKeyError:
      raise NotFound
  else:
    data = model.get_by_key_name(item)
  if data:
    data = data.get()
  else:
    raise NotFound
  return 200, dict(data=data), {}

def head(request, model, item):
  return get(request, model, item)

def post(request, model, item):
  if item != None:
    raise
  elif isinstance(item, int):
    data = model.get_by_id(item)
  else:
    data = model.get_by_key_name(item)
  if data:
    data = data.get()
  else:
    raise NotFound
  return 200, dict(data=request.environ["REQUEST_METHOD"]), {}

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
  return json.dumps(data), "text/json"

def format_yaml(data):
  import yaml
  return yaml.dump(data, default_flow_style=False), "text/yaml"

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

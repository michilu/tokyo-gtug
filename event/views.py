# -*- coding: utf-8 -*-
import logging

from google.appengine.api import users
from google.appengine.api import memcache
from werkzeug import (
  unescape, redirect, Response,
)
from werkzeug.exceptions import (
  NotFound, MethodNotAllowed, BadRequest
)

from kay.utils import (
  render_to_response, reverse,
  get_by_key_name_or_404, get_by_id_or_404,
  to_utc, to_local_timezone, url_for, raise_on_dev
)
from kay.i18n import gettext as _
from kay.auth.decorators import login_required

method = lambda request, model: dict(data=request.environ["REQUEST_METHOD"])
methods = {
  "HEAD": method,
  "GET": method,
  "POST": method,
  "PUT": method,
  "DELETE": method,
  "OPTIONS": method,
  "TRACE": method,
}

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
  def func(request, format="yaml"):
    method = request.environ["REQUEST_METHOD"]
    if method in methods:
      result, mimetype = formater[format](methods[method](request, model))
    else:
      raise
    return Response(_(result if result.endswith("\n") else "%s\n" % result),
                      mimetype=mimetype)
  return func

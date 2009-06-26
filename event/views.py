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

method = lambda request, model: request.environ["REQUEST_METHOD"]
methods = {
  "HEAD": method,
  "GET": method,
  "POST": method,
  "PUT": method,
  "DELETE": method,
  "OPTIONS": method,
  "TRACE": method,
}

def rest(model, methods=methods, acl=None):
  mimetype = "text/yaml"
  def func(request, format="yaml"):
    if format == "json":
      import simplejson as json
      mimetype = "text/json"
    else:
      import yaml
      mimetype = "text/yaml"
    method = request.environ["REQUEST_METHOD"]
    if method in methods:
      result = methods[method](request, model)
    else:
      raise
    return Response(_(str("%s: %s\n" % (result, format))),
                      mimetype=mimetype)
  return func

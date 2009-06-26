# -*- coding: utf-8 -*-
# event.views

import logging

import simplejson as json
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

# Create your views here.

def index(request):
  return render_to_response('event/index.html', {'message': _('Hello')})

def rest(model):
  mimetype = "text/json"
  def func(request, format="json"):
    message = request.environ.keys()
    if request.environ["REQUEST_METHOD"] == "HEAD":
      message = "HEAD"
    elif request.environ["REQUEST_METHOD"] == "GET":
      message = "GET"
    elif request.environ["REQUEST_METHOD"] == "POST":
      message = "POST"
    elif request.environ["REQUEST_METHOD"] == "PUT":
      message = "PUT"
    elif request.environ["REQUEST_METHOD"] == "DELETE":
      message = "DELETE"
    elif request.environ["REQUEST_METHOD"] == "OPTIONS":
      message = "OPTIONS"
    elif request.environ["REQUEST_METHOD"] == "TRACE":
      message = "TRACE"
    else:
        raise
    return Response(_(str("%s: %s" % (message, format))),
                      mimetype=mimetype)
  return func

# -*- coding: utf-8 -*-
# event.urls

"""
Bellow is an easy example to mount this event application.

------------------------------------
from event import urls as event_urls

def make_url():
  return Map([
    Submount('/event', event_urls.make_rules())
  ])

all_views = {
}
all_views.update(event_urls.all_views)

------------------------------------

"""

from werkzeug.routing import (
  Map, Rule, Submount,
  EndpointPrefix, RuleTemplate,
)
import event.views
import event.models

resource = RuleTemplate([
    Rule('/$resource', endpoint='$resource'),
    Rule('/$resource.<format>', endpoint='$resource'),
    Rule('/$resource/<int:item>', endpoint='$resource'),
    Rule('/$resource/<int:item>.<format>', endpoint='$resource'),
    Rule('/$resource/<item>', endpoint='$resource'),
    Rule('/$resource/<item>.<format>', endpoint='$resource'),
])

def make_rules():
  return [
    resource(resource='event'),
  ]

all_views = {
  'event': event.views.rest(event.models.Event),
}

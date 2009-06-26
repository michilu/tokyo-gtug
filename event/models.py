# -*- coding: utf-8 -*-
# event.models

from google.appengine.ext import db
from kay.utils.forms.modelform import ModelForm

class Event(db.Model):
    title = db.StringProperty(required=True)
    summary = db.StringProperty()
    discription = db.TextProperty(required=True)
    start = db.StringProperty(required=True)
    end = db.DateTimeProperty(auto_now_add=False)
    limit = db.IntegerProperty()
    place = db.StringProperty()
    address = db.StringProperty()
    url = db.LinkProperty()
    comment = db.StringProperty(required=True)
    image = db.Blob()
    #option = 

class MyForm(ModelForm):
    class Meta:
        model = Event


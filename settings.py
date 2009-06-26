# -*- coding: utf-8 -*-

"""
A sample of kay settings.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import os

DEFAULT_TIMEZONE = 'Asia/Tokyo'
DEBUG = True
PROFILE = False
SECRET_KEY = 'hogehoge'
SESSION_PREFIX = 'gaesess:'
COOKIE_AGE = 1209600 # 2 weeks
COOKIE_NAME = 'KAY_SID'

ADD_APP_PREFIX_TO_KIND = True

ADMINS = (
  ['Takashi Matsuo', 'tmatsuo@shehas.net'],
)

TEMPLATE_DIRS = (
  'templates',
)

USE_I18N = True
DEFAULT_LANG = 'en'

INSTALLED_APPS = (
  'kay.sessions',
)

MIDDLEWARE_CLASSES = (
  'kay.sessions.middleware.SessionMiddleware',
  'kay.auth.middleware.GoogleAuthenticationMiddleware',
)

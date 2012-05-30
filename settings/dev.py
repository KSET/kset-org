from __future__ import absolute_import
from .base import *


DEBUG = True
#TEMPLATE_DEBUG = DEBUG

SECRET_KEY = 'g4(a#vl07uj2tna)^g=!d%@e*2k#=o1*pf*2f4re)5!saad^jh'


DATABASES = { 
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'kset-dev',                      # Or path to database file if using sqlite3.
        'USER': 'kset',                      # Not used with sqlite3.
        'PASSWORD': 'kset123',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5433',                      # Set to empty string for default. Not used with sqlite3.
    }   
}


AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',
)


MEDIA_URL = 'http://www.kset.loc/media/'
FILEBROWSER_MEDIA_URL = MEDIA_URL


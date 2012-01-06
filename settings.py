# Django settings for kset project.

from local_settings import *

ADMINS = (
  ('Veljko Dragsic', 'veljko@kset.org'),
)

MANAGERS = ADMINS

TIME_ZONE = 'Europe/Zagreb'
LANGUAGE_CODE = 'hr-hr'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

ROOT_URLCONF = 'kset.urls'

ANONYMOUS_USER_ID = -1

PREPEND_WWW = True

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.request',
    'ctx.header',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'tagging',
    'tagging_autocomplete',
    'filebrowser',
    'grappelli',
    'django.contrib.admin',

    'events',
    'news',
    'subpages',
    'search',
    'members',
    'newsletter',
    'savjet',
    'zivpdf',
    'guardian',
    'gallery',

)


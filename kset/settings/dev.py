from django.conf import global_settings
from .base import *


DEBUG = TEMPLATE_DEBUG = True

PREPEND_WWW = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dev.db',
    }
}

# We need to use Postgres because of PG Array support
try:
    import dj_database_url
    DATABASES = {'default': dj_database_url.config(
        default='postgres://kset:kset@localhost:5432/ksetdb')}
except ImportError:
    pass

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


AUTHENTICATION_BACKENDS = global_settings.AUTHENTICATION_BACKENDS +\
    ('django.contrib.auth.backends.ModelBackend',)


# Disable caching while in development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# set up Django Debug Toolbar if installed
try:
    import debug_toolbar  # noqa
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TOOLBAR_CALLBACK': lambda *args, **kwargs: True
    }
except ImportError:
    pass


LOGGING = BASE_LOGGING

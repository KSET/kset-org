# Django settings for kset project.
from os.path import abspath, join, dirname

PROJECT_DIR = abspath(join(dirname(__file__), '..'))

ADMINS = (
  ('Veljko Dragsic', 'veljko@kset.org'),
  ('Deni Bertovic', 'deni@kset.org')
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

# Additional locations of static files
STATICFILES_DIRS = ( 
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = ( 
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


STATIC_ROOT = join(PROJECT_DIR, 'media','static')
STATIC_URL = '/media/static/'

MEDIA_ROOT = join(PROJECT_DIR, 'media/')
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"
TEMPLATE_DIRS = (
    join(PROJECT_DIR, 'templates'),
    join(PROJECT_DIR, 'templates','members_templates'),
)

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
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.contrib.messages.context_processors.messages',
    'ctx.header',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tagging',
    'tinymce',
    'tagging_autocomplete',
    'grappelli.dashboard',
    'grappelli',
    'filebrowser',
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

GRAPPELLI_ADMIN_TITLE = 'kset.org'
GRAPPELLI_INDEX_DASHBOARD = 'kset.dashboard.CustomIndexDashboard'

FILEBROWSER_URL_TINYMCE = '/media/static/tiny_mce/'
FILEBROWSER_PATH_TINYMCE = join(PROJECT_DIR, 'media/static/tiny_mce/')
FILEBROWSER_MEDIA_ROOT = MEDIA_ROOT

TAGGING_AUTOCOMPLETE_JS_BASE_URL = '/media/js/jquery-autocomplete'


# tinymce settings, add/remove buttons and so on
TINYMCE_DEFAULT_CONFIG = {
'theme': "advanced",
'theme_advanced_toolbar_location' : "top",
'theme_advanced_resizing' : True,
'plugins' : 'table,contextmenu,paste,autoresize,media,lists,style',
#'height' : 600,
#'width' : 800,
#'theme_advanced_resize_horizontal' : True,
'theme_advanced_buttons1': "style, bold,italic,underline,separator,bullist,separator,outdent,indent,separator,undo,redo, image, link",
'theme_advanced_buttons2': "cleanup,lists,pasteword,table,contextmenu,media",
'theme_advanced_buttons3': "",
}


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}



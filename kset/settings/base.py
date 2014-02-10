# Django settings for kset project.
from django.conf import global_settings
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PROJECT_NAME = os.path.basename(ROOT_DIR)


def ABS_PATH(*args):
    return os.path.join(ROOT_DIR, *args)

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

ANONYMOUS_USER_ID = -1
USE_TZ = True

PREPEND_WWW = True

# Additional locations of static files
STATICFILES_DIRS = (
    ABS_PATH('staticfiles'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


STATIC_ROOT = ABS_PATH('static')
STATIC_URL = '/static/'


MEDIA_ROOT = ABS_PATH('media')

MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

TEMPLATE_DIRS = (
    ABS_PATH('templates'),
    ABS_PATH('templates', 'members_templates'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = PROJECT_NAME + '.urls'

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS +\
    ('django.core.context_processors.request',
     'ctx.header')


def ensure_secret_key_file():
    """Checks that secret.py exists in settings dir. If not, creates one
    with a random generated SECRET_KEY setting."""
    secret_path = os.path.join(ABS_PATH('settings'), 'secret.py')
    if not os.path.exists(secret_path):
        from django.utils.crypto import get_random_string
        secret_key = get_random_string(50,
            'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
        with open(secret_path, 'w') as f:
            f.write("SECRET_KEY = " + repr(secret_key) + "\n")

# Import the secret key
ensure_secret_key_file()
from secret import SECRET_KEY

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'tinymce',
    'grappelli.dashboard',
    'grappelli',
    'filebrowser',
    'django.contrib.admin',

    'south',

    'events',
    'news',
    'subpages',
    'search',
    'members',
    'newsletter',
    'savjet',
    'gallery',

)

GRAPPELLI_ADMIN_TITLE = 'kset.org'
GRAPPELLI_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'

FILEBROWSER_URL_TINYMCE = '/static/tiny_mce/'
FILEBROWSER_PATH_TINYMCE = ABS_PATH('media', 'static', 'tiny_mce')
FILEBROWSER_MEDIA_ROOT = MEDIA_ROOT

FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg', '.JPG', '.JPEG', '.jpeg', '.gif', '.png', '.tif', '.tiff'],
    'Video': ['.mov', '.wmv', '.mpeg', '.mpg', '.avi', '.rm'],
    'Document': ['.pdf', '.doc', '.rtf', '.txt', '.xls', '.csv'],
    'Audio': ['.mp3', '.mp4', '.wav', '.aiff', '.midi', '.m4p'],
    'Code': ['.html', '.py', '.js', '.css']
}

FILEBROWSER_SELECT_FORMATS = {
    'File': ['Folder', 'Document'],
    'Image': ['Folder', 'Image'],
    'Media': ['Video', 'Sound'],
    'Document': ['Document'],
    # for TinyMCE we can also define lower-case items
    'image': ['Image'],
    'file': ['Folder', 'Image', 'Document'],
}

FILEBROWSER_VERSIONS = {
    'fb_thumb': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60,
        'opts': 'crop upscale'},
    'thumbnail': {'verbose_name': 'Thumbnail (140px)', 'width': 140,
        'height': '', 'opts': ''},
    'small': {'verbose_name': 'Small (80x60px)', 'width': 80,
        'height': '60', 'opts': 'crop'},
    'medium': {'verbose_name': 'Medium (100px)', 'width': 100,
        'height': '', 'opts': ''},
    'semibig': {'verbose_name': 'SemiBig (420px)', 'width': 420,
        'height': '', 'opts': ''},
    'big': {'verbose_name': 'Big (465px)', 'width': 465, 'height': '', 'opts': ''},
    'event_big': {'verbose_name': 'Event Thumbnail Big (370px)', 'width': 370,
        'height': 370, 'opts': 'crop upscale'},
    'event_small': {'verbose_name': 'Event Thumbnail Small (70px)',
        'width': 70, 'height': 70, 'opts': 'crop upscale'},
    'gallerytb': {'verbose_name': 'gallery_thumbnail (255px)', 'width': 255,
        'height': 173, 'opts': 'crop'},
    'sticky': {'verbose_name': 'Main Page Sticky (150px)', 'width': 150,
        'height': 80, 'opts': 'crop'},
    'galleryimage': {'verbose_name': 'gallery_image (800x600)',
        'width': '', 'height': 600, 'opts': ''},

}

# Versions available within the Admin-Interface.
FILEBROWSER_ADMIN_VERSIONS = ['thumbnail', 'small', 'medium', 'semibig',
    'big', 'event_small', 'event_big']
# Which Version should be used as Admin-thumbnail.
FILEBROWSER_ADMIN_THUMBNAIL = 'fb_thumb'

FILEBROWSER_DEFAULT_SORTING_BY = 'filename_lower'


# tinymce settings, add/remove buttons and so on
TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'theme_advanced_toolbar_location': "top",
    'theme_advanced_resizing': True,
    'plugins': 'table,contextmenu,paste,autoresize,media,lists,style',
    'theme_advanced_buttons1': str("style,bold,italic,underline,separator,"
        "bullist,separator,outdent,indent,separator,undo,redo,image,link"),
    'theme_advanced_buttons2': "cleanup,lists,pasteword,table,contextmenu,media,code",
    'theme_advanced_buttons3': "",
}

LOGIN_URL = '/admin/'

BASE_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler'
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

LOGGING = BASE_LOGGING

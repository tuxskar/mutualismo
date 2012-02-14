# coding=utf-8
from os import path


DEBUG = True
TEMPLATE_DEBUG = DEBUG
BASE_DIR = path.normpath(path.dirname(__file__))

ADMINS = (
    ('Alejandro', 'alejandrogomez@gmail.com'),
    ('Esteban',   'fadoro@gmail.com'),
    ('Óscar',     'tuxskar@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE':   'sqlite3', 
        'NAME':     path.join(BASE_DIR, 'database.db'),                      
        'USER':     '',
        'PASSWORD': '',                  
        'HOST':     '',                  
        'PORT':     '',                  
    }
}

TIME_ZONE = 'Europe/Madrid'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = path.join(BASE_DIR, 'media')
MEDIA_URL  = '/media'

STATIC_ROOT        = path.join(BASE_DIR, 'static')
STATIC_URL         = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'nz^nz&lu2o46v#b^k5y7%p09gcgf&z^#^b+!jb$jhakx4oe6%_'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth', 
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'mutualismo.urls'

PROJECT_TEMPLATES = path.join(BASE_DIR, 'templates')
RED_TEMPLATES = path.join(BASE_DIR, 'red/templates')
TEMPLATE_DIRS = (
    PROJECT_TEMPLATES,
    RED_TEMPLATES
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django_autoslug',
    'registration',
    'faq',
    'taggit',
    'django_autoslug',
    'django_nose',
    'haystack',
    'red',
)

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

# Search
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': path.join(path.dirname(__file__), 'whoosh_index'),
    },
}

# Registration
ACCOUNT_ACTIVATION_DAYS = 7

# Testing
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=red',
]

# Debugging

# Fake email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = path.join(BASE_DIR, 'tmp')

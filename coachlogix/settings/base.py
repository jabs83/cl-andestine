"""
This is the base settings file for Coachlogix API.

Do not use this file directly, rather you should pull these settings
in through the appropriate environment settings. The environment
settings files should set environment-specific settings to override
the values in this file.

To activate your environment:

    1) Create a symbolic link called `active.py` in the settings/env
       directory. This link should point to one of the following:
           
           a) env/dev.py
           b) env/uat.py
           c) env/production.py

    2) For settings that should only be applied to the local development
       environment, create a settings/local.py file and add them there.

    3) Be sure to only modify  the environment settings for environment-
       specific values.

"""
import os
import sys

from django.utils.translation import ugettext_lazy as _
from datetime import timedelta, datetime

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__name__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+_wjdsy12@jl_=a*6=+1h(z*qw^9^e4s=hr@*eg_nv(@(wnhq6'


# Debug
DEBUG = False
TEMPLATE_DEBUG = False


# Site settings
ALLOWED_HOSTS = []
ROOT_URLCONF = 'coachlogix.urls'
WSGI_APPLICATION = 'coachlogix.wsgi.application'
BASE_APP_URL = 'http://localhost:8080/'
APPEND_SLASH = False


# Application definition
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
LOCAL_APPS = (
    'coachlogix.apps.engagements',
    'coachlogix.apps.accounts',
    'coachlogix.apps.files',
    'coachlogix.apps.generic',
    'coachlogix.apps.organizations',
    'coachlogix.apps.users',
)
THIRD_PARTY_APPS = (
    'easy_thumbnails',
    'rest_framework',
)

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS


# Authentication
AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)


# Middleware
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


# Databases
DATABASES = {
    'default': {},
}


# Cache settings
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static-media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static-media')
STATICFILES_DIRS = ()
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'coachlogix/templates'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
)


# Django-rest-framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_ember.parsers.EmberJSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_ember.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PAGINATION_SERIALIZER_CLASS': (
        'rest_framework_ember.pagination.EmberPaginationSerializer',
    ),
}


# rest_framework_ember
REST_EMBER_FORMAT_KEYS = True
REST_EMBER_PLURALIZE_KEYS = True


# Box.com API settings
BOX_API_KEY = ''
BOX_SESSION_DURATION = ''


# File settings
def get_upload_path(instance, filename):
    return datetime.now().strftime(
        '{}/%Y/%m/%d/{}'.format(instance.__class__.__name__.lower(), filename))
GET_UPLOAD_PATH = get_upload_path

VALID_DOCUMENT_EXTENSIONS = (
    'pdf',
    'doc',
    'docx',
    'xlsx',
    'pptx',
    'ppsx',
    'sldx',
)
VALID_IMAGE_EXTENSIONS = (
    'jpeg',
    'jpg',
    'png',
    'gif',
)
VALID_DOCUMENT_MIMETYPES = (
    'application/pdf',
    'application/zip',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.template',
    'application/vnd.openxmlformats-officedocument.presentationml.template',
    'application/vnd.openxmlformats-officedocument.presentationml.slideshow',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/vnd.openxmlformats-officedocument.presentationml.slide',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
)
VALID_IMAGE_MIMETYPES = (
    'image/jpg',
    'image/jpeg',
)
VALID_FILE_EXTENSIONS = VALID_DOCUMENT_EXTENSIONS + VALID_IMAGE_EXTENSIONS
VALID_FILE_MIMETYPES = VALID_DOCUMENT_MIMETYPES + VALID_IMAGE_MIMETYPES


# Easy-Thumbnails settings
THUMBNAIL_ALIASES = {
    '': {
        'x-small': {'size': (25, 25), 'crop': 'smart'},
        'small': {'size': (50, 50), 'crop': 'smart'},
        'large': {'size': (500, 0), 'crop': 'scale'},
        'default': {'size': (200, 200), 'crop': 'smart'},
    }
}
THUMBNAIL_DEFAULT_ALIAS = 'default'
THUMBNAIL_BASEDIR = 'thumbnails'
THUMBNAIL_HIGHRES_INFIX = '_2x'
THUMBNAIL_HIGH_RESOLUTION = True
THUMBNAIL_NAMER = 'easy_thumbnails.namers.source_hashed'
THUMBNAIL_SOURCE_GENERATORS = (
    'easy_thumbnails.source_generators.pil_image',
)

# Provider settings
PROVIDER_EXTENSIONS = (
    'pdf',
    'doc',
    'docx',
    'pptx',
    'ppt'
)

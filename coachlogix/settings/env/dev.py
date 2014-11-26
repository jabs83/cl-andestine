"""
This is the development settings file for Coachlogix API.

All settings and overrides that are specific for team-wide
development should be put here.

For settings that should be used only with the local dev,
use a settings/local.py file.
"""
import os
from ..base import *


# Debug
DEBUG = True


# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}


# Cache settings
CACHES['default'].update({
    'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
})

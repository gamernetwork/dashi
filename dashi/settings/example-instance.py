from defaults import *

DEBUG = True
FAKE = False

from scaffolding import *

ALLOWED_HOSTS = [
    '*',
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'applog': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': './dashi.log'
        },

    },
    'loggers': {
        'django': {
            'handlers': ['applog'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['applog'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db': {
            'handlers': ['applog'],
            'level': 'ERROR',
            'propagate': False,
        },
        'dashi': {
            'handlers': ['applog'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

VERSION = '20180712151932'
STATICLINK_VERSION = '20180712151932'

ADMINS = (
    ('Mark Kennedy', 'mark@gamer-network.net'),
)

MANAGERS = ADMINS

TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en_GB'
SITE_ID = 1

# generate this 
SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

from dashboard import *

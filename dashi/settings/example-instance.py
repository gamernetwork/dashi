from defaults import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DAJAXICE_DEBUG = DEBUG
# fake the update data instead of fetching from memcache
FAKE = True

from scaffolding import *

ADMINS = (
    ('Mark Kennedy', 'mark@eurogamer.net'),
)

MANAGERS = ADMINS

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'dajaxice': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'
SITE_ID = 1

# generate this
SECRET_KEY = 'blahlfdkgfkbjdk'

# import block config
from dashboard import *

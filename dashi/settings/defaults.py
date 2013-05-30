DEBUG = False
TEMPLATE_DEBUG = DEBUG
FAKE = False
DAJAXICE_DEBUG = DEBUG

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

import os
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
STATIC_ROOT = os.path.join(SITE_ROOT, '.collectedstatic' )
STATIC_URL = "/static/"
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static' ),
)

TEMPLATE_DIRS = (
    os.path.join( SITE_ROOT, 'templates' ),
)

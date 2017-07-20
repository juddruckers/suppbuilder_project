from .base import *

DEBUG = False

ALLOWED_HOSTS = ['162.243.151.222']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DBNAME'),
	'USER': os.environ.get('DBUSER'),
	'PASSWORD' : os.environ.get('DBKEY'),
	'HOST' : 'localhost',
	'PORT' : '',
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get('EMAIL_HOST'),
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587

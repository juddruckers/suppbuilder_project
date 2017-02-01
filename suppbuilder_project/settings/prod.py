from . settings import *

SECRET_KEY = os.environ.get('SECRETKEY')

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

"""
Django settings for suppbuilder_project project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
# import pdb
# pdb.set_trace()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# BASE_DIR = '/Users/Judd/suppbuilder_project/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

                
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRETKEY')

# Application definition

INSTALLED_APPS = [
    'suppbuilder.apps.SuppbuilderConfig',
    'products.apps.ProductsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'carton',
    'shopping',
    'crispy_forms',
]


CART_PRODUCT_MODEL = 'products.models.Variation'

LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/suppbuilder'

SITE_ID=1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'suppbuilder_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)


WSGI_APPLICATION = 'suppbuilder_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

#ALL AUTH SETTINGS
# path to custom sign up form to have first and last name instead of username

ACCOUNT_ADAPTER = 'suppbuilder.adapter.AccountAdapter'

# user must enter password twice to avoid typos
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE =True

#disables the need username field
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

#settings pointing to custom sign up form
ACCOUNT_SIGNUP_FORM_CLASS = 'suppbuilder.forms.SignupForm'

# username not required
ACCOUNT_USERNAME_REQUIRED = False

#user is required to provide email account when signing up
ACCOUNT_EMAIL_REQUIRED = True

#prevents a user from signing up using an email address if that address is already used
ACCOUNT_UNIQUE_EMAIL = True

# setting that disables the intermediate sign out page
ACCOUNT_LOGOUT_ON_GET = True

#sign in using email
ACCOUNT_AUTHENTICATION_METHOD = "email"

#settings for django crispy form
CRISPY_TEMPLATE_PACK = 'bootstrap3'


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'suppbuilder_project': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}




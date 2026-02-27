from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-appd@dm2(duc1xm%tzyt-@rsj)1kds1)pj(3n=c94lxn-vp#r("


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_db',
        'USER': 'django_user',
        'PASSWORD': 'pass',
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE': 60,
}
}
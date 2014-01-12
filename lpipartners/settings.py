"""
Django settings for lpipartners project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DIRNAME = os.path.abspath(os.path.dirname(__file__))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zadnteivgu$(sugy*1uc99x^qh(^k8t+6r98qdz0bz@)czx(eo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True
TEMPLATE_DIRS = (
   os.path.join(DIRNAME, '../templates'),
)



ALLOWED_HOSTS = []

AUTHENTICATION_BACKENDS  = (
    'django.contrib.auth.backends.ModelBackend',
    'redmineauth.backends.Redmine',
)


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_redmine',
    'partners'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'lpipartners.urls'

WSGI_APPLICATION = 'lpipartners.wsgi.application'

X_FRAME_OPTIONS = 'ALLOW-FROM http://tortuga'



# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


# API KEYS
REDMINE_URL = 'http://desk.lpi-italia.org' # no trailing slash
REDMINE_API = ''
REDMINE_PROJECT = 'lpi-partership'

CHARGIFY_API = 'VRatXKPQ3OaPhnc8oe5i'
CHARGIFY_SUBDOMAIN = 'metaforge-test1'

CHARGIFY_HOSTED_PAGE = "https://%s.chargify.com/h/" % CHARGIFY_SUBDOMAIN



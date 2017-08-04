"""
Django settings for football_tools project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z!=tm!f=&&fqhjt6n4%2kt^2tk-d0(3b9@n=!v$)$eq%7203%d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

FOOTBALL_TOOL_APPS = (
    'core',
    'draft_bot'
)

INSTALLED_APPS += FOOTBALL_TOOL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'football_tools.urls'

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

WSGI_APPLICATION = 'football_tools.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASS'],
        'HOST': "127.0.0.1",
        'PORT': 5432,
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "{0}/{1}".format(os.environ.get('REDIS_URL'), 0),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,  # mimics memcache behavior.
                                        # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
        }
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# ------------------------------------------------------
# Fantasy Football Point Settings
# ------------------------------------------------------

PASSING_TD_POINTS = 4
PASSING_YD_POINTS = 1.0 / 25
PASSING_INT_POINTS = -2
RUSHING_TD_POINTS = 6
RUSHING_YD_POINTS = 1.0 / 10
RECEIVING_YD_POINTS = 1.0 / 10
RECEIVING_TD_POINTS = 6
RECEIVING_REC_POINTS = 0.5

# ------------------------------------------------------
# League / Rosters
# ------------------------------------------------------

from collections import namedtuple

LeagueConfig = namedtuple('LeagueConfig', ['draft_position', 'keepers'])
# dont want to use actual model here, just something easy to set up in settings
Player = namedtuple('Player', ['name', 'playerid'])

LEAGUE_SETTINGS = {
    "Chris": LeagueConfig(1, []),
    "John": LeagueConfig(2, []),
    "Andy": LeagueConfig(3, []),
    "Tara": LeagueConfig(4, []),
    "Dan": LeagueConfig(5, []),
    "Jason": LeagueConfig(6, []),
    "Finck": LeagueConfig(7, []),
    "Jim": LeagueConfig(8, []),
    "Harry": LeagueConfig(9, []),
    "Brad": LeagueConfig(10, []),
    "Anthony": LeagueConfig(11, []),
    "Megan": LeagueConfig(12, []),
}

# will mark players as injuired when building new draft
INJURIES = [

]

# give valued rookies a point boost
GOOD_ROOKIES = [
]

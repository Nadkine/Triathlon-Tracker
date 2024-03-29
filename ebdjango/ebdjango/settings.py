"""
Django settings for ebdjango project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = ""
with open('PrivateSettings.txt','r') as f:
    for line in f.read().splitlines(): 
        SECRET_KEY = line

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['triathlontracker-dev.eu-central-1.elasticbeanstalk.com', 'localhost.com','localhost', '44.237.60.194','strava.tjeerdsantema.nl', 
                '18.193.158.161','172.31.31.18','127.0.0.1','52.40.71.97', '18.192.229.48','85.147.12.166','192.168.178.43', '0.0.0.0',
                'triathlon-tracker.com', '3.70.215.154','172.31.47.101','ec2-3-70-215-154.eu-central-1.compute.amazonsaws.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'activities',
    'users', 
    'crispy_forms',
    'pages',
    'graph',
    'user_profile',
    'friends'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ebdjango.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")],
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

WSGI_APPLICATION = 'ebdjango.wsgi.application'


# Database
with open('DatabasePassword.txt','r') as f:
    for line in f.read().splitlines(): 
        password = line
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# DATABASES = {
#     'default': {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': 'TriathlonTracker',
#     'USER': 'tjeerdsje',
#     'PASSWORD': password,
#     'HOST': 'aa1fl9fjn6qg5kv.cj43pzf7zuhv.eu-central-1.rds.amazonaws.com',
#     'PORT': '5432',
#     'ATOMIC_REQUESTS': True
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '/tmp/memcached.sock',
    }
}
# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

TATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

CRISPY_TEMPLATE_PACK = 'bootstrap4' 

LOGIN_REDIRECT_URL = '/start' 

os.environ['MPLCONFIGDIR'] = os.getcwd() + "/configs/"

"""
Django settings for business project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
import datetime

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.http import response

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!9%qwcecrp57s9!zbe6ul=app$s@ibp1395)y0uhl8@c(&3i68'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
BY_PASS_ARM = False
Z_LIMIT = -25
ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True
# Application definition

# python manage.py rqworker default low

CHANNEL_LAYERS = {
    "default": {
        "CONFIG": {
            "hosts": [('localhost', '6379')]
        },
        "BACKEND": 'channels_redis.core.RedisChannelLayer'
    }
}

RQ_QUEUES = {
    'default': {
        'HOST': '192.168.1.6',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 10000,
    }, 'stir_fry': {
        'HOST': '192.168.1.6',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 10000,
    }, 'deep_fry': {
        'HOST': '192.168.1.6',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 10000,
    }, 'grilling': {
        'HOST': '192.168.1.6',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 10000,
    }, 'drinks': {
        'HOST': '192.168.1.6',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 10000,
    }, 'boiler': {
        'HOST': '192.168.1.6',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 10000,
    }, 'steaming': {
        'HOST': '192.168.1.6',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 10000,
    },
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'app',
    'computer_vision',
    'rest_framework',
    'django_rq',
    'channels',
    'ui'
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.FileUploadParser'
    ),
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'business.urls'

JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
        'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
        'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
        'rest_framework_jwt.utils.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
        'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'rest_framework_jwt.utils.jwt_response_payload_handler',

    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_AUTH_COOKIE': None,

}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'business.wsgi.application'
ASGI_APPLICATION = 'business.asgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

MEDIA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(MEDIA_DIR, 'static_files')]
STATIC_ROOT = os.path.join(MEDIA_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(MEDIA_DIR, 'media')

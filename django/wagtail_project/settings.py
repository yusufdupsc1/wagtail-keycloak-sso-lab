"""
Django settings for wagtail-sso-lab project.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET', 'dev-secret-key')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Wagtail (v5+)
    'wagtail',
    'wagtail.admin',
    'wagtail.snippets',
    'wagtail.users',
    'wagtail.images',
    'wagtail.documents',
    'wagtail.search',
    'taggit',
    
    # Third party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    
    # Local
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'wagtail_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'wagtail_project.wsgi.application'

# Database - use SQLite for local testing
import os
if os.environ.get('DATABASE_URL', '').startswith('sqlite'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB', 'wagtail'),
            'USER': os.environ.get('POSTGRES_USER', 'wagtail'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'wagtail_pass'),
            'HOST': os.environ.get('POSTGRES_HOST', 'postgres'),
            'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Wagtail
WAGTAIL_SITE_NAME = 'Wagtail SSO Lab'

# Django Allauth with Keycloak
KEYCLOAK_URL = os.environ.get('KEYCLOAK_URL', 'http://localhost:8080')
KEYCLOAK_REALM = os.environ.get('KEYCLOAK_REALM', 'wagtail-realm')

SOCIALACCOUNT_PROVIDERS = {
    'keycloak': {
        'KEYCLOAK_URL': KEYCLOAK_URL,
        'KEYCLOAK_REALM': KEYCLOAK_REALM,
        'APP': {
            'client_id': os.environ.get('KEYCLOAK_CLIENT_ID', 'wagtail-app'),
            'secret': os.environ.get('KEYCLOAK_CLIENT_SECRET', ''),
        }
    }
}

SOCIALACCOUNT_ADAPTER = 'accounts.adapters.KeycloakSocialAccountAdapter'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

SITE_ID = 1

# Session (Django 4.x)
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'allauth': {'handlers': ['console'], 'level': 'DEBUG'},
        'django.security': {'handlers': ['console'], 'level': 'DEBUG'},
    },
}

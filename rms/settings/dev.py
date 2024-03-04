from .base import *

DEBUG=True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "secret_key+bro"

ALLOWED_HOSTS = ["*"]

# EMAILS
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache_table",
    }
}

# Databases
DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
    }
}
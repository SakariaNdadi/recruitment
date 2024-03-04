from .base import *
from dotenv import load_dotenv
import os
load_dotenv()

DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']
# ALLOWED_HOSTS = [os.environ["ALLOWED_HOSTS"]]
ALLOWED_HOSTS = ["127.0.0.0", "0.0.0.0"]
CSRF_TRUSTED_ORIGINS = ["https://" + os.environ["ALLOWED_HOSTS"]]

ADMINS = [
    ('Sakaria Ndadi', 'sakariandadi@gmail.com'),
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ['DB_NAME'],
        "USER": os.environ['DB_USER'],
        "PASSWORD": os.environ['DB_PASSWORD'],
        "HOST": os.environ['DB_HOST'],
        "PORT": os.environ['DB_PORT'],
    }
}

# Cache and Sessions
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
    }
}
REDIS_URL = 'redis://cache:6379'
CACHES['default']['LOCATION'] = REDIS_URL


# EMAILS
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_USE_TLS = os.environ['EMAIL_USE_TLS']
EMAIL_PORT = os.environ['EMAIL_PORT']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

# SECURITY
X_FRAME_OPTIONS = "DENY"
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 3600
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# Recaptcha
RECAPTCHA_PUBLIC_KEY = os.environ['RECAPTCHA_PUBLIC_KEY']
RECAPTCHA_PRIVATE_KEY = os.environ['RECAPTCHA_PRIVATE_KEY']
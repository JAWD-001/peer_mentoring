from decouple import config
from django.conf.global_settings import CACHES

from .base import *  # noqa

DEBUG = False

ADMINS = [
    ("James", "dycus.j.jd@gmail.com"),
]

ALLOWED_HOSTS = ["*", "bondedbrotherhood.com", "www.bondedbrotherhood.com"]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": "db",
        "PORT": 5432,
    }
}

REDIS_URL = "redis://cache:6379"
CHANNEL_LAYERS["default"]["CONFIG"]["hosts"] = [REDIS_URL]  # noqa
CACHES["default"]["LOCATION"] = REDIS_URL

# Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

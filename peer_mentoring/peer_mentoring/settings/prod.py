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
        "ENGINE": config("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": config("SQL_DATABASE", BASE_DIR / "db.sqlite3"),  # noqa
        "USER": config("SQL_USER", "user"),
        "PASSWORD": config("SQL_PASSWORD", "password"),
        "HOST": config("SQL_HOST", "localhost"),
        "PORT": config("SQL_PORT", "5432"),
    }
}

REDIS_URL = "redis://cache:6379"
CHANNEL_LAYERS["default"]["CONFIG"]["hosts"] = [REDIS_URL]  # noqa
CACHES["default"]["LOCATION"] = REDIS_URL

# Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

from .base import *

"""
Tests settings are suitable for a running pytest inside docker containers
- DEBUG = True
- Postgres containers as database backend
- No cache settings (redis)
- No celery settings
- Local storage for django files (media/static)
"""

print(f"Loading Django tests settings (docker)")

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": static_settings.POSTGRES_DB,
        "USER": static_settings.POSTGRES_USER,
        "PASSWORD": static_settings.POSTGRES_PASSWORD,
        "HOST": static_settings.POSTGRES_HOST,
        "PORT": static_settings.POSTGRES_PORT,
    }
}

# FILE STORAGE
STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_URL = "/" + static_settings.MEDIA_URL + "/"
MEDIA_ROOT = os.path.join(BASE_DIR, static_settings.MEDIA_URL)
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

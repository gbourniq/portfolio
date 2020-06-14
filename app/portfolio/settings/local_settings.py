from .base import *

"""
Local settings are suitable for a baremetal deployment:
- DEBUG = True
- Local postgres
- No Email backend configuration
- No cache settings (redis)
- No celery settings
- Local storage for django files (media/static)
"""

print(f"Loading Django {static_settings.BUILD} settings")

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": static_settings.POSTGRES_DB,
        "USER": static_settings.POSTGRES_USER,
        "PASSWORD": static_settings.POSTGRES_PASSWORD,
        "HOST": "localhost",
        "PORT": static_settings.POSTGRES_PORT,
    }
}

# FILE STORAGE
STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_URL = "/" + static_settings.MEDIA_URL + "/"
MEDIA_ROOT = os.path.join(BASE_DIR, static_settings.MEDIA_URL)
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

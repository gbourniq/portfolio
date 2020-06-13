from .base import *

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

"""
Django settings for portfolio project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from app import static_settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = static_settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = static_settings.DEBUG

ALLOWED_HOSTS = static_settings.ALLOWED_HOSTS

TINYMCE_DEFAULT_CONFIG = {
    "height": 360,
    "width": 1120,
    "cleanup_on_startup": True,
    "custom_undo_redo_levels": 20,
    "selector": "textarea",
    "theme": "modern",
    "plugins": """
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            """,
    "toolbar1": """
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            """,
    "toolbar2": """
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            """,
    "contextmenu": "formats | link image",
    "menubar": True,
    "statusbar": True,
}

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_results",
    "main",
    "tinymce",
    "materializecssform",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "portfolio.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "portfolio.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Cache configuration
# Cache time to live is 15 mn.
CACHE_TTL = 5 * 1
if static_settings.REDIS_HOST:
    print("Loading Redis Cache settings")
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": f"redis://{static_settings.REDIS_HOST}:{static_settings.REDIS_PORT}/1",
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
            "KEY_PREFIX": "example",
        }
    }

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
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

# CELERY CONFIGURATION
# https://blog.syncano.rocks/configuring-running-django-celery-docker-containers-pt-1/
if static_settings.REDIS_HOST:
    # Set Redis as Broker URL
    BROKER_URL = (
        f"redis://{static_settings.REDIS_HOST}:{static_settings.REDIS_PORT}/2"
    )

    # Set django-redis as celery result backend
    CELERY_RESULT_BACKEND = "django-db"
    CELERY_REDIS_MAX_CONNECTIONS = 1

    # Sensible settings for celery
    CELERY_ALWAYS_EAGER = False
    CELERY_ACKS_LATE = True
    CELERY_TASK_PUBLISH_RETRY = True
    CELERY_DISABLE_RATE_LIMITS = False

    # By default we will ignore result
    # If you want to see results and try out tasks interactively, change it to False
    # Or change this setting on tasks level
    CELERY_IGNORE_RESULT = False
    CELERY_SEND_TASK_ERROR_EMAILS = False
    CELERY_TASK_RESULT_EXPIRES = 600

    # configure queues, currently we have only one
    CELERY_DEFAULT_QUEUE = "default"
    # CELERY_QUEUES = (
    #     Queue('default', Exchange('default'), routing_key='default'),
    # )


# FILE STORAGE
if static_settings.ENABLE_S3_FOR_DJANGO_FILES:
    # aws s3 settings for django
    AWS_ACCESS_KEY_ID = static_settings.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = static_settings.AWS_SECRET_ACCESS_KEY
    AWS_STORAGE_BUCKET_NAME = static_settings.AWS_STORAGE_BUCKET_NAME
    AWS_DEFAULT_REGION = static_settings.AWS_DEFAULT_REGION
    AWS_DEFAULT_ACL = None
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    AWS_S3_CUSTOM_DOMAIN = (
        f"s3.{AWS_DEFAULT_REGION}.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}"
    )
    # s3 static settings
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/django_files/static/"
    STATICFILES_STORAGE = "main.storage_backends.StaticStorage"
    # s3 public media settings
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/django_files/media/"
    DEFAULT_FILE_STORAGE = "main.storage_backends.PublicMediaStorage"
else:
    STATIC_URL = "/staticfiles/"
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    MEDIA_URL = "/" + static_settings.MEDIA_URL + "/"
    MEDIA_ROOT = os.path.join(BASE_DIR, static_settings.MEDIA_URL)

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)


# Email parameters
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = static_settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = static_settings.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = True
EMAIL_TIMEOUT = 10


# Configuration which writes all logging from the django logger to a local file
if static_settings.LOGGING_ENABLED:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s %(levelname)s %(name)s %(message)s"
            },
        },
        "handlers": {
            "file": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": "info.log",
                "formatter": "standard",
            },
        },
        "loggers": {
            "": {"handlers": ["file"], "level": "INFO", "propagate": True},
        },
    }

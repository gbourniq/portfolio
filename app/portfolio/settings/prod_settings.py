from .base import *

print(f"Loading Django {static_settings.BUILD} settings")

DEBUG = False

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

# Cache configuration
# Cache time to live is 15 mn.
CACHE_TTL = 5 * 1
print("Loading Redis Cache settings")
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{static_settings.REDIS_HOST}:{static_settings.REDIS_PORT}/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "example",
    }
}

# CELERY CONFIGURATION
# https://blog.syncano.rocks/configuring-running-django-celery-docker-containers-pt-1/
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

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

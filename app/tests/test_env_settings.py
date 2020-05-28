import importlib
from os import getenv
from typing import Dict

from app import static_settings
from app.portfolio import settings


class TestDjangoSettingsRedis:
    """
    Class to test that settings.py is configured correctly
    when running the app with Celery/Redis
    """

    static_settings.REDIS_HOST = "redis"
    importlib.reload(settings)

    def test_cache_settings(self):
        """
        Test the cache settings are loaded
        """
        assert settings.CACHES == {
            "default": {
                "BACKEND": "django_redis.cache.RedisCache",
                "LOCATION": "redis://redis:6379/1",
                "OPTIONS": {
                    "CLIENT_CLASS": "django_redis.client.DefaultClient"
                },
                "KEY_PREFIX": "example",
            }
        }

    def test_celery_settings(self):
        """
        Test the celery settings are loaded
        """
        assert all(
            hasattr(settings, attr)
            for attr in [
                "CELERY_RESULT_BACKEND",
                "CELERY_REDIS_MAX_CONNECTIONS",
                "CELERY_ALWAYS_EAGER",
                "CELERY_ACKS_LATE",
                "CELERY_TASK_PUBLISH_RETRY",
                "CELERY_DISABLE_RATE_LIMITS",
                "CELERY_SEND_TASK_ERROR_EMAILS",
                "CELERY_TASK_RESULT_EXPIRES",
                "CELERY_DEFAULT_QUEUE",
            ]
        )


class TestDjangoSettingsS3:
    """
    Class to test that settings.py is configured correctly
    when running the app using S3 for file storage (static/media files)
    """

    static_settings.ENABLE_S3_FOR_DJANGO_FILES = True
    importlib.reload(settings)

    def test_aws_settings(self):
        """
        Test the AWS settings are loaded
        """
        assert settings.AWS_ACCESS_KEY_ID == getenv("AWS_ACCESS_KEY_ID")
        assert settings.AWS_SECRET_ACCESS_KEY == getenv("AWS_SECRET_ACCESS_KEY")
        assert settings.AWS_STORAGE_BUCKET_NAME == getenv(
            "AWS_STORAGE_BUCKET_NAME"
        )
        assert settings.AWS_DEFAULT_REGION == getenv("AWS_DEFAULT_REGION")

        assert all(
            hasattr(settings, attr)
            for attr in [
                "AWS_DEFAULT_ACL",
                "AWS_S3_OBJECT_PARAMETERS",
                "AWS_S3_CUSTOM_DOMAIN",
                "STATIC_URL",
                "STATICFILES_STORAGE",
                "MEDIA_URL",
                "DEFAULT_FILE_STORAGE",
            ]
        )


class TestDjangoSettingsLogging:
    """
    Class to test that settings.py is configured correctly
    when enabling logging
    """

    static_settings.LOGGING_ENABLED = True
    importlib.reload(settings)

    def test_cache_settings(self):
        assert all(hasattr(settings, attr) for attr in ["LOGGING",])
        assert isinstance(settings.LOGGING, Dict)

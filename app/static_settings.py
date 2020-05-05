import os

"""
This file collects environment variables across the repo and store them into global
variables. This allows to easily update the code base if in the future a variable
is renamed or removed.
"""

# ======================= SETTINGS.PY =========================

# General settings
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG")
ALLOWED_HOSTS = [os.getenv("ALLOWED_HOSTS")]

# Postgres
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
POSTGRES_DB = os.getenv("POSTGRES_DB", "portfoliodb")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

# Optional - Message Broker for Celery workers
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)

# Email details for contact us page
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# Save logs to log.info
LOGGING_ENABLED = os.getenv("LOGGING_ENABLED") == "True"

# ==================== AWS ======================

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
S3_STORAGE_ENABLED = os.getenv("S3_STORAGE_ENABLED") == "True"

# ======================= CHECK ENV VARIABLES ARE SET =========================


ENV_VARS = [
    "SECRET_KEY",
    "DEBUG",
    "ALLOWED_HOSTS",
    "POSTGRES_HOST",
    "POSTGRES_PORT",
    "POSTGRES_DB",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "EMAIL_HOST_USER",
    "EMAIL_HOST_PASSWORD",
]

if S3_STORAGE_ENABLED:
    ENV_VARS += [
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_STORAGE_BUCKET_NAME",
        "AWS_DEFAULT_REGION",
    ]


for ENV_VAR in ENV_VARS:
    if not locals().get(ENV_VAR):
        raise EnvironmentError(
            f"The {ENV_VAR} environment variable has not been "
            "set. Please set this environment variable."
        )

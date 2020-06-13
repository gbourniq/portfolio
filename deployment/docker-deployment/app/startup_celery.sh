#!/bin/sh

cd /home/portfoliouser/portfolio/app

echo "Setting DJANGO_SETTINGS_MODULE to portfolio.settings.docker_settings"
export DJANGO_SETTINGS_MODULE=portfolio.settings.docker_settings

echo "Starting celery worker"
celery --app=portfolio.celeryconf worker --loglevel=info --concurrency=10 -n worker1.%h
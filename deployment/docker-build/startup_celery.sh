#!/bin/sh

cd ${DOCKER_PORTFOLIO_APP_DIR}/

celery --app=portfolio.celeryconf worker --loglevel=info --concurrency=10 -n worker1.%h
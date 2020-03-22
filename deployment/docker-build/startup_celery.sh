#!/bin/sh

cd /home/portfolio/app/

celery --app=portfolio.celeryconf worker --loglevel=info --concurrency=10 -n worker1.%h
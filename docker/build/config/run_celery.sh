#!/bin/sh

cd myproject  
# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
su -m myuser -c "celery worker -A myproject.celeryconf -Q default -n default@%h"  


# "celery worker --app=worker.worker.app --concurrency=1 --hostname=worker_1@%h --loglevel=INFO"
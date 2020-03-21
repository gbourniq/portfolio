#!/bin/sh

# run Celery worker with unpriviledged user for our portfolio project with Celery configuration stored in celeryconf
cd /home/portfolio/app/

celery --app=portfolio.celeryconf worker --loglevel=info --concurrency=10 -n worker1.%h

# Production: run with unpriviledge user
# su -m celery-user -c "celery worker -A portfolio.celeryconf -n worker1.%h"

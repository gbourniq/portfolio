FROM redis:alpine

RUN apk add --no-cache bash

COPY /deployment/build-images/config/run_redis_healthcheck.sh /usr/local/bin/


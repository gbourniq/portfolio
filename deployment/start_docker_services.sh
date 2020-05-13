#!/bin/sh


# This file is used by an ubuntu Crontab (crontab -e) to run app on instance start up.
# The crontab includes the following entry:
# @reboot /home/ubuntu/portfolio/deployment/start_docker_services.sh
# This expects the project root directory to be named `portfolio`

cd portfolio/deployment

source .env

cd docker-deployment

docker-compose ${COMPOSE_ARGS} up -d

cd ../../..
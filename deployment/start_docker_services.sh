#!/bin/bash


# This file is used by an ubuntu Crontab (crontab -e) to run app on instance start up.
# The crontab includes the following entry:
# @reboot /home/ubuntu/portfolio/deployment/start_docker_services.sh

source .env

cd docker-deployment

docker-compose ${COMPOSE_ARGS} up -d
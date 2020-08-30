#!/bin/bash

# Exit on error
set -e

if [[ -z $BUILD ]] || \
   [[ -z $COMPOSE_ARGS ]]
then
  exit_error "Some of the following environment variables are not set: \
BUILD, COMPOSE_ARGS. Aborting."
fi

INFO "[BUILD=${BUILD}] Removing docker-compose services..."
cd deployment/docker-deployment
docker-compose ${COMPOSE_ARGS} down --remove-orphans || true
cd -
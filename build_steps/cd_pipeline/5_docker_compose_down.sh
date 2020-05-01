#!/bin/bash

# Exit on error
set -e

INFO "[BUILD=${BUILD}] Removing docker-compose services..."
cd deployment/docker-deployment
docker-compose ${COMPOSE_ARGS} down --remove-orphans || true
cd -
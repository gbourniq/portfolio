#!/bin/bash

# Exit on error
set -e

# Set traps to clean up if exit or something goes wrong
trap "echo 'Something went wrong! Tidying up...' && remove_services && exit 1" ERR

# Helper function: Exit with error
function exit_error() {
  ERROR "$1" 1>&2
  exit 1
}

function validate_environment_variables() {
  if [[ -z $BUILD ]] || \
     [[ -z $IMAGE_REPOSITORY ]] || \
     [[ -z $COMPOSE_ARGS ]]
  then
    exit_error "Some of the following environment variables are not set: \
BUILD, IMAGE_REPOSITORY, COMPOSE_ARGS. Aborting."
  fi
}

function remove_services() {
  INFO "[BUILD=${BUILD}] Removing docker-compose services..."
  docker-compose ${COMPOSE_ARGS} down --remove-orphans || true
}

function start_services() {
  INFO "[BUILD=${BUILD}] Starting docker-compose services with ${IMAGE_REPOSITORY}:latest."
  docker-compose ${COMPOSE_ARGS} up -d
  # docker-compose ${COMPOSE_ARGS} up -d app
}



### Start script
validate_environment_variables
cd deployment/docker-deployment
remove_services
start_services
cd -
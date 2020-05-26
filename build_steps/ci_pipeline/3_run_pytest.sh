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

function build_test_image() {
  docker build -f deployment/docker-build/tests.Dockerfile -t ${IMAGE_REPOSITORY}:tests .
  SUCCESS "${IMAGE_REPOSITORY}:tests built successfully"
}

function run_tests() {
  if ! (docker exec -it app-tests sh -c "cd app && pytest --cov")
  then
      exit_error "Some tests have failed! Aborting."
  fi
}

function remove_services() {
  INFO "[BUILD=${BUILD}] Removing docker-compose services..."
  docker-compose ${COMPOSE_ARGS} down --remove-orphans || true
}

function start_services() {
  INFO "[BUILD=${BUILD}] Starting docker-compose services with ${IMAGE_REPOSITORY}:tests."
  docker-compose ${COMPOSE_ARGS} up -d
}

### Set environment variables for testing
BUILD=tests
PROJECT_NAME=portfolio-tests
COMPOSE_FILE=deployment/docker-deployment/tests.docker-compose.yml
COMPOSE_ARGS="-p ${PROJECT_NAME} -f ${COMPOSE_FILE}"

### Start script
build_test_image
remove_services
start_services
source ./scripts/check_services_health.sh
run_tests
remove_services
SUCCESS "Run tests successfully with pytest-django" 




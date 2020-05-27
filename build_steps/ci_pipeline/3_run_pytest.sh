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
  docker build -f deployment/docker-build/${BUILD}.Dockerfile -t ${IMAGE_REPOSITORY}:tests .
  SUCCESS "${IMAGE_REPOSITORY}:tests built successfully"
}

function remove_services() {
  INFO "[BUILD=${BUILD}] Removing docker-compose services..."
  docker-compose ${COMPOSE_ARGS} down --remove-orphans || true
}

function start_services() {
  INFO "[BUILD=${BUILD}] Starting docker-compose services with ${IMAGE_REPOSITORY}:tests."
  docker-compose ${COMPOSE_ARGS} up -d
}

function run_test_with_docker() {

  INFO "Running tests with containers... (POSTGRES_HOST=postgres)"

  ### Set environment variables for testing with docker
  BUILD=tests
  PROJECT_NAME=portfolio-tests
  COMPOSE_FILE=deployment/docker-deployment/tests.docker-compose.yml
  COMPOSE_ARGS="-p ${PROJECT_NAME} -f ${COMPOSE_FILE}"

  build_test_image
  remove_services
  start_services
  source ./scripts/check_services_health.sh
  if ! (docker exec -it app-tests sh -c "cd app && pytest --cov=. --cov-report=term-missing -vx")
  then
      exit_error "Some tests have failed! Aborting."
  fi
  remove_services
}

function run_test_locally() {

  INFO "Running tests locally... (POSTGRES_HOST=localhost)"

  source $(conda info --base)/etc/profile.d/conda.sh

  if [[ -z $CONDA_ENV_NAME ]]; then
    exit_error "CONDA_ENV_NAME not set! Aborting."
  fi
  conda activate ${CONDA_ENV_NAME}

  if ! (pytest --cov=. --cov-report=term-missing -vx)
  then
      exit_error "Some tests have failed! Aborting."
  fi
}


# Start script
  if [[ $POSTGRES_HOST == "localhost" ]]; then
    cd app
    run_test_locally
    cd -
  elif [[ $POSTGRES_HOST == "postgres" ]]; then
    run_test_with_docker
    SUCCESS "Congrats! All tests passed successfully! 💯" 
  else
    exit_error "$POSTGRES_HOST not set! Aborting."
  fi




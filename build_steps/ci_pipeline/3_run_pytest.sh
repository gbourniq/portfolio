#!/bin/bash

# Exit on error
set -e

# Set traps to clean up if exit or something goes wrong
# trap "echo 'Something went wrong! Tidying up...' && remove_services && exit 1" ERR

# Helper function: Exit with error
function exit_error() {
  ERROR "$1"
  remove_tests_services
  exit 1
}

function get_container_id() {
  docker-compose $1 ps -q $2
}

function get_service_health() {
  container_id=$(get_container_id "$1" "$2")
  echo ${container_id} | xargs -I ID docker inspect -f '{{if .State.Running}}{{ .State.Health.Status }}{{end}}' ID
}

function check_service_health() {
  until [[ $(get_service_health "$1" "$2") != "starting" ]]; do
    sleep 1
  done;
  if [[ $(get_service_health "$1" "$2") != "healthy" ]]; then
    exit_error "$2 failed health check"
  else
    echo ⭐️ $2 healthy ⭐️;
  fi;
}

function build_test_image() {
  docker build -f deployment/docker-build/${BUILD}.Dockerfile -t ${IMAGE_REPOSITORY}:tests .
  SUCCESS "${IMAGE_REPOSITORY}:tests built successfully"
}

function remove_tests_services() {
  INFO "[BUILD=${BUILD}] Removing docker-compose services..."
  docker-compose ${COMPOSE_ARGS} down --remove-orphans || true
}

function start_services() {
  INFO "[BUILD=${BUILD}] Starting docker-compose services with ${IMAGE_REPOSITORY}:tests."
  docker-compose ${COMPOSE_ARGS} up -d
}

function run_test_with_docker() {

  INFO "Running tests inside containers..."

  ### Set environment variables for testing with docker
  BUILD=tests
  PROJECT_NAME=portfolio-tests
  COMPOSE_FILE=deployment/docker-deployment/tests.docker-compose.yml
  COMPOSE_ARGS="-p ${PROJECT_NAME} -f ${COMPOSE_FILE}"

  build_test_image
  remove_tests_services
  start_services

  services=(postgres)
  for service_name in ${services[*]}; do
    check_service_health "${COMPOSE_ARGS}" "$service_name"
  done

  if ! (docker exec -it app-tests sh -c "cd portfolio/app/ && pytest --cov=. --cov-report=term-missing -x")
  then
      exit_error "Some tests have failed! Aborting."
  fi
  remove_tests_services
}

function run_test_locally() {

  INFO "Running tests locally..."

  source $(conda info --base)/etc/profile.d/conda.sh

  if [[ -z $CONDA_ENV_NAME ]]; then
    exit_error "CONDA_ENV_NAME not set! Aborting."
  fi
  conda activate ${CONDA_ENV_NAME}

  if ! (pytest --cov=. --cov-report=term-missing -x)
  then
      exit_error "Some tests have failed! Aborting."
  fi
}


# Start script
  # if [[ $RUN_TESTS_WITH_DOCKER == "False" ]]; then
  #   cd app
  #   run_test_locally
  #   cd -
  # fi

  run_test_with_docker
  SUCCESS "Congrats! All tests passed successfully! 💯" 



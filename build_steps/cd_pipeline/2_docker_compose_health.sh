#!/bin/bash

# Exit on error
set -ex

# Set traps to clean up if exit or something goes wrong
trap "echo 'Something went wrong! Tidying up...' && remove_services && exit 1" ERR

# Helper function: Exit with error
function exit_error() {
  ERROR "$1" 1>&2
  exit 1
}

# Define functions
function get_container_id() {
  echo $(docker-compose $1 ps -q $2)
}

function get_service_health() {
  container_id=$(get_container_id "$1" "$2")
  echo $(echo ${container_id} | xargs -I ID docker inspect -f '{{if .State.Running}}{{ .State.Health.Status }}{{end}}' ID)
}

function check_service_health() {
  until [[ $(get_service_health "$1" "$2") != "starting" ]]; do
    sleep 1
  done;
  if [[ $(get_service_health "$1" "$2") != "healthy" ]]; then
    exit_error "$2 failed health check"
  else
    echo $2 healthy!;
  fi;
}

function start_services() {
  INFO "[BUILD=${BUILD}] Starting docker-compose services with ${IMAGE_REPOSITORY}:latest."
  docker-compose ${COMPOSE_ARGS} up -d
  docker-compose ${COMPOSE_ARGS} up -d app
}

function check_all_services_health() {
  INFO "[BUILD=${BUILD}] Checking services health..."
  services=("postgres" "redis" "app" "worker")
  for service_name in ${services[*]}; do
    check_service_health "${COMPOSE_ARGS}" "$service_name"
  done
  SUCCESS "All services are up and healthy"
}

function remove_services() {
  INFO "[BUILD=${BUILD}] Removing docker-compose services..."
  docker-compose ${COMPOSE_ARGS} down --remove-orphans || true
  SUCCESS "[BUILD=${BUILD}] All cleaned up!"
}


### Start script
cd deployment/docker-deployment

builds=("dev" "prod")

for build in ${builds[*]}; do
  export BUILD="$build"
  start_services
  check_all_services_health
  remove_services
done

cd -

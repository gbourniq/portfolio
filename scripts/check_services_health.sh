#!/bin/bash

# Set traps to clean up if exit or something goes wrong
trap "echo 'Something went wrong! Tidying up...' && remove_services && exit 1" ERR

# Helper function: Exit with error
function exit_error() {
  ERROR "$1" 1>&2
  exit 1
}

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

# Start script
cd deployment/docker-deployment
INFO "Checking services health for ${BUILD} build..."

if [[ ${BUILD} == dev ]]; then
    services=(postgres redis app worker)
elif [[ ${BUILD} == prod ]]; then
    services=(postgres redis app worker nginx)
else
    exit_error "Unknown build type: ${BUILD}"
fi

for service_name in ${services[*]}; do
    check_service_health "${COMPOSE_ARGS}" "$service_name"
done

SUCCESS "All services are up and healthy"
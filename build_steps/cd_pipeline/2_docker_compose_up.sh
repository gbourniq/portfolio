#!/bin/bash

# Define function for services healthcheck
get_container_id() {
  echo $(docker-compose $1 ps -q $2)
}
export -f get_container_id

get_service_health() {
  container_id=$(get_container_id "$1" "$2")
  echo $(echo ${container_id} | xargs -I ID docker inspect -f '{{if .State.Running}}{{ .State.Health.Status }}{{end}}' ID)
}

check_service_health() {
  until [[ $(get_service_health "$1" "$2") != "starting" ]]; do
    sleep 1
  done;
  if [[ $(get_service_health "$1" "$2") != "healthy" ]]; then
    echo $2 failed health check;
    exit 1
  else
    echo $2 healthy!;
  fi;
}

export BUILD=dev 

INFO "[BUILD=${BUILD}] Starting docker-compose services with ${IMAGE_REPOSITORY}:latest."
cd deployment/docker-deployment
docker-compose ${COMPOSE_ARGS} up -d

INFO "[BUILD=${BUILD}] Checking services health..."
check_service_health "${COMPOSE_ARGS}" postgres
check_service_health "${COMPOSE_ARGS}" redis
check_service_health "${COMPOSE_ARGS}" app
check_service_health "${COMPOSE_ARGS}" worker
SUCCESS "All services are up and healthy"

INFO "[BUILD=${BUILD}] Removing docker-compose services..."
cd deployment/docker-deployment && docker-compose ${COMPOSE_ARGS} down --remove-orphans
SUCCESS "[BUILD=${BUILD}] All cleaned up!"


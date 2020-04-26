#!/bin/bash

# Exit on error
set -e

# Set traps to clean up if exit or something goes wrong
trap "echo 'Something went wrong! Tidying up...' && remove_services && exit 1" ERR
trap "echo 'Tidying up...' && remove_services && exit 0" EXIT

# Helper function: Exit with error
function exit_error() {
  ERROR "$1" 1>&2
  exit 1
}

start_services() {
  INFO "[BUILD=${BUILD}] Starting docker-compose services with ${IMAGE_REPOSITORY}:latest."
  docker-compose ${COMPOSE_ARGS} up -d
}

get_service_health() {
  container_id=$(get_container_id "$1" "$2")
  echo $(echo ${container_id} | xargs -I ID docker inspect -f '{{if .State.Running}}{{ .State.Health.Status }}{{end}}' ID)
}

check_service_health() {
  until [[ $(get_service_health "$1" "$2") != "starting" ]]; do
    sleep 1
  done;
  if [[ $(get_service_health "$1" "$2") != "healthy" ]]; then
    exit_error "$2 failed health check"
  else
    echo $2 healthy!;
  fi;
}

remove_services() {
  INFO "[BUILD=${BUILD}] Removing docker-compose services..."
  docker-compose ${COMPOSE_ARGS} down --remove-orphans || true
}

postgres_dump_to_s3_test() {
  INFO "Create and upload postgres backup to ${S3_POSTGRES_BACKUP_URI}/cd_test"
  ./scripts/postgres_dump_to_s3.sh ${POSTGRES_CONTAINER_NAME} ${POSTGRES_DB} ${S3_POSTGRES_BACKUP_URI}/cd_test
  DUMP_TO_S3_STATE=$?
  if [ "$DUMP_TO_S3_STATE" -ne 0 ]; then
    exit_error "Postgres backup failed! Aborting."
  fi
  SUCCESS "Postgres dump uploaded to ${S3_POSTGRES_BACKUP_URI}/cd_test"
}

postgres_restore_from_s3_test() {
  INFO "Restore latest postgres backup from ${S3_POSTGRES_BACKUP_URI}/cd_test"
  ./scripts/postgres_restore_from_s3.sh ${POSTGRES_CONTAINER_NAME} ${POSTGRES_DB} ${S3_POSTGRES_BACKUP_URI}/cd_test
  RESTORE_FROM_S3_STATE=$?
  if [ "$RESTORE_FROM_S3_STATE" -ne 0 ]; then
    exit_error "Postgres restore failed! Aborting."
  fi
  SUCCESS "Latest postgres dump restored from ${S3_POSTGRES_BACKUP_URI}/cd_test/"
}

### Start script
cd deployment/docker-deployment
start_services
check_service_health "${COMPOSE_ARGS}" postgres
cd -
postgres_dump_to_s3_test
postgres_restore_from_s3_test
cd -
remove_services
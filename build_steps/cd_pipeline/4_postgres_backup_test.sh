#!/bin/bash

# Exit on error
set -e


# Helper function: Exit with error
function exit_error() {
  ERROR "$1" 1>&2
  exit 1
}

function validate_environment_variables() {
  if [[ -z $S3_POSTGRES_BACKUP_URI ]] || \
     [[ -z $POSTGRES_DB ]]
  then
    exit_error "Some of the following environment variables are not set: \
S3_POSTGRES_BACKUP_URI, POSTGRES_DB. Aborting."
  fi
}

function postgres_dump_to_s3_test() {
  INFO "Create and upload postgres backup to ${S3_POSTGRES_BACKUP_URI}/cd_pipeline"
  if ! (./scripts/postgres_dump_to_s3.sh postgres ${POSTGRES_DB} ${S3_POSTGRES_BACKUP_URI}/cd_pipeline)
  then
    exit_error "Postgres backup failed! Aborting."
  fi
  SUCCESS "Postgres dump uploaded to ${S3_POSTGRES_BACKUP_URI}/cd_pipeline"
}

function postgres_restore_from_s3_test() {
  INFO "Restore latest postgres backup from ${S3_POSTGRES_BACKUP_URI}/cd_pipeline"
  if ! (./scripts/postgres_restore_from_s3.sh postgres ${POSTGRES_DB} ${S3_POSTGRES_BACKUP_URI}/cd_pipeline)
  then
    exit_error "Postgres restore failed! Aborting."
  fi
  SUCCESS "Latest postgres dump restored from ${S3_POSTGRES_BACKUP_URI}/cd_pipeline"
}

### Start script
if [[ $AWS_ENABLED != True ]]; then
  INFO "AWS_ENABLED not set to True. Postgres back up set is skipped."
  exit 0
fi
validate_environment_variables
postgres_dump_to_s3_test
postgres_restore_from_s3_test
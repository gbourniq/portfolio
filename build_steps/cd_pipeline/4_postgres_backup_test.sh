#!/bin/bash

# Exit on error
set -e


# Helper function: Exit with error
function exit_error() {
  ERROR "$1" 1>&2
  exit 1
}

function postgres_dump_to_s3_test() {
  INFO "Create and upload postgres backup to ${S3_POSTGRES_BACKUP_URI}/cd_test"
  ./scripts/postgres_dump_to_s3.sh postgres ${POSTGRES_DB} ${S3_POSTGRES_BACKUP_URI}/cd_test
  DUMP_TO_S3_STATE=$?
  if [ "$DUMP_TO_S3_STATE" -ne 0 ]; then
    exit_error "Postgres backup failed! Aborting."
  fi
  SUCCESS "Postgres dump uploaded to ${S3_POSTGRES_BACKUP_URI}/cd_test"
}

function postgres_restore_from_s3_test() {
  INFO "Restore latest postgres backup from ${S3_POSTGRES_BACKUP_URI}/cd_test"
  ./scripts/postgres_restore_from_s3.sh postgres ${POSTGRES_DB} ${S3_POSTGRES_BACKUP_URI}/cd_test
  RESTORE_FROM_S3_STATE=$?
  if [ "$RESTORE_FROM_S3_STATE" -ne 0 ]; then
    exit_error "Postgres restore failed! Aborting."
  fi
  SUCCESS "Latest postgres dump restored from ${S3_POSTGRES_BACKUP_URI}/cd_test/"
}

### Start script
postgres_dump_to_s3_test
postgres_restore_from_s3_test
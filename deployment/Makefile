# Set shell
SHELL=/bin/bash -e -o pipefail


.PHONY: up down postgres-dump-to-s3 postgres-restore-from-s3

up: env-validation
	@ docker-compose ${COMPOSE_ARGS} up -d

down: env-validation
	@ docker-compose ${COMPOSE_ARGS} down --remove-orphans || true

postgres-dump-to-s3: env-validation
	@ INFO "Create and upload postgres backup to AWS S3"
	@ ../scripts/postgres_dump_to_s3.sh postgres ${POSTGRES_DB} ${S3_POSTGRES_BACKUP_URI}/

postgres-restore-from-s3: env-validation
	@ INFO "Download postgres dump from S3 and restore database"
	@ ../scripts/postgres_restore_from_s3.sh postgres ${POSTGRES_DB} ${S3_POSTGRES_BACKUP_URI}/


.PHONY: env-validation

env-validation:
	@ INFO "Checking if required environment variables are set..."
	@ ../scripts/env_validation.sh
	@ SUCCESS "All good!"
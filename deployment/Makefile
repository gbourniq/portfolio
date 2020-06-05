# Set shell
SHELL=/bin/bash -e -o pipefail


.PHONY: up down postgres-dump-to-s3 postgres-restore-from-s3 helm-deploy

up: env-validation
	@ cd docker-deployment/ && docker-compose ${COMPOSE_ARGS} up -d

check-services-health: env-validation
	@ cd docker-deployment && ../../scripts/check_services_health.sh

down: env-validation
	@ cd docker-deployment/ && docker-compose ${COMPOSE_ARGS} down --remove-orphans || true

postgres-dump-to-s3: env-validation
	@ INFO "Create and upload postgres backup to AWS S3"
	@ ../scripts/postgres_dump_to_s3.sh postgres ${POSTGRES_DB} ${S3_POSTGRES_BACKUP_URI}

postgres-restore-from-s3: env-validation
	@ INFO "Download postgres dump from S3 and restore database"
	@ ../scripts/postgres_restore_from_s3.sh postgres ${POSTGRES_DB} ${S3_POSTGRES_BACKUP_URI}

helm-deploy:
	@ ./kubernetes/scripts/deploy_helm.sh

.PHONY: env-validation

env-validation:
	@ ../scripts/env_validation.sh


# ----------------------------------------------------
#
# Check all variables are set with non-empty values
#
# ----------------------------------------------------
# Params:
#   1. Variable name(s) to test.
#   2. (optional) Error message to print.
check_defined = \
    $(strip $(foreach 1,$1, \
        $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
      $(error Undefined $1$(if $2, ($2))))

$(call check_defined, COMPOSE_ARGS, Please source .env)
$(call check_defined, POSTGRES_DB, Please source .env)
$(call check_defined, S3_POSTGRES_BACKUP_URI, Please source .env)
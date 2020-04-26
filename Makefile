# Set shell
SHELL=/bin/bash -e -o pipefail


# ----------------------------------------------------
#
# CI SCRIPTS
#
# ----------------------------------------------------
.PHONY: env pre-commit lint-code unit-tests recreatedb

ci-all: env pre-commit lint-code unit-tests recreatedb

env:
	@ ./build_steps/ci_pipeline/1_set_environment.sh
	@ MESSAGE "Please activate the conda environment and source your environment variables:"
	@ MESSAGE "- conda activate ${CONDA_ENV_NAME}"
	@ MESSAGE "- source .env"

pre-commit:
	@ pre-commit install -t pre-commit -t commit-msg
	@ SUCCESS "pre-commit set up"

lint-code: 
	@ ./build_steps/ci_pipeline/2_lint_code.sh

unit-tests: 
	@ ./build_steps/ci_pipeline/3_run_pytest.sh

recreatedb:
	@ INFO "Re-create postgres, migrations and dummy superuser"
	@ . ./scripts/reset_all.sh


# ----------------------------------------------------
#
# CD SCRIPTS
#
# ----------------------------------------------------
.PHONY: cd-all image-latest image-tagged check-compose-health-dev-prod publish-latest publish-tagged docker-deploy-tarball up postgres-backup-test down run-ansible-playbook

cd-all: image-latest image-tagged check-compose-health-dev-prod publish-latest publish-tagged docker-deploy-tarball up postgres-backup-test down run-ansible-playbook

image-latest:
	@ ./build_steps/cd_pipeline/1_build_image.sh

image-tagged:
	@ ./build_steps/cd_pipeline/1_build_image.sh tagged

check-compose-health-dev-prod:
	@ ./build_steps/cd_pipeline/2_docker_compose_health.sh

publish-latest:
	@ ./build_steps/cd_pipeline/3_push_docker_image.sh

publish-tagged:
	@ ./build_steps/cd_pipeline/3_push_docker_image.sh tagged

docker-deploy-tarball:
	@ ./build_steps/cd_pipeline/4_build_and_push_docker_compose_tarball.sh

up:
	@ . .env
	@ ./build_steps/cd_pipeline/5_docker_compose_up.sh

postgres-backup-test:
	@ ./build_steps/cd_pipeline/6_postgres_backup_test.sh

down:
	@ ./build_steps/cd_pipeline/7_docker_compose_down.sh

run-ansible-playbook:
	@ ./build_steps/cd_pipeline/8_run_ansible_playbooks.sh


# ----------------------------------------------------
#
# POSTGRES BACKUP
#
# ----------------------------------------------------
.PHONY: postgres-dump-to-s3 postgres-restore-from-s3

postgres-dump-to-s3:
	@ INFO "Create and upload postgres backup to AWS S3"
	@ ./scripts/postgres_dump_to_s3.sh ${POSTGRES_CONTAINER_NAME} ${POSTGRES_DB} ${S3_POSTGRES_BACKUP_URI}/

postgres-restore-from-s3:
	@ INFO "Download postgres dump from S3 and restore database"
	@ ./scripts/postgres_restore_from_s3.sh ${POSTGRES_CONTAINER_NAME} ${POSTGRES_DB} ${S3_POSTGRES_BACKUP_URI}/


# ----------------------------------------------------
#
# UTILS
#
# ----------------------------------------------------
# Ensure all environment variables are set
.PHONY: env-validation
env-validation:
	@ INFO "Checking if required environment variables are set..."
	@ ./scripts/env_validation.sh
	@ SUCCESS "All good!"

# Ensure environment variable is set
check-%:
	@ if [ "${${*}}" = "" ]; then \
        echo "Environment variable $* not set"; \
        exit 1; \
    fi
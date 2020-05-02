# Set shell
SHELL=/bin/bash -e -o pipefail


# ----------------------------------------------------
#
# CI SCRIPTS
#
# ----------------------------------------------------
.PHONY: env pre-commit lint-code unit-tests recreatedb

ci-all: env pre-commit lint-code unit-tests

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


# ----------------------------------------------------
#
# CD SCRIPTS
#
# ----------------------------------------------------
.PHONY: cd-all image-latest image-tagged up check-services-health postgres-backup-test down publish-latest publish-tagged docker-deploy-tarball-custom run-ansible-playbook

cd-all: env-validation image-latest image-tagged up check-services-health postgres-backup-test down publish-latest publish-tagged docker-deploy-tarball-custom run-ansible-playbook

image-latest:
	@ ./build_steps/cd_pipeline/1_build_image.sh

image-tagged:
	@ ./build_steps/cd_pipeline/1_build_image.sh tagged

up:
	@ ./build_steps/cd_pipeline/2_docker_compose_up.sh

check-services-health:
	@ ./build_steps/cd_pipeline/3_check_services_health.sh

postgres-backup-test:
	@ ./build_steps/cd_pipeline/4_postgres_backup_test.sh

down:
	@ ./build_steps/cd_pipeline/5_docker_compose_down.sh

publish-latest:
	@ ./build_steps/cd_pipeline/6_push_docker_image.sh

publish-tagged:
	@ ./build_steps/cd_pipeline/6_push_docker_image.sh tagged

docker-deploy-tarball-custom:
	@ ./build_steps/cd_pipeline/7_build_and_push_docker_compose_tarball.sh ${S3_DOCKER_DEPLOY_TARBALL_CUSTOM}

run-ansible-playbook:
	@ ./build_steps/cd_pipeline/8_run_ansible_playbooks.sh


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

recreatedb:
	@ INFO "Re-create postgres, migrations and dummy superuser"
	@ . ./scripts/reset_local_db.sh


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

$(call check_defined, CONDA_ENV_NAME, Please source .dev.env)
$(call check_defined, S3_DOCKER_DEPLOY_TARBALL_CUSTOM, Please source .dev.env)
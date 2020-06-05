# Set shell
SHELL=/bin/bash -e -o pipefail


# This Makefile allows to trigger the CI and CD pipelines, as well as individual steps

# ----------------------------------------------------
#
# CI/CD Pipeline
#
# ----------------------------------------------------
.PHONY: run-ci-pipeline run-cd-pipeline run-ci-cd-pipeline

run-ci-cd-pipeline: run-ci-pipeline run-cd-pipeline

run-ci-pipeline:
	@ ./build_steps/run_ci_pipeline.sh

run-cd-pipeline:
	@ ./build_steps/run_cd_pipeline.sh


# ----------------------------------------------------
#
# CI STEPS
#
# ----------------------------------------------------
.PHONY: env pre-commit lint recreatedb

env:
	@ ./build_steps/ci_pipeline/1_set_environment.sh
	@ INFO "Please activate the conda environment and source your environment variables:"
	@ MESSAGE "- conda activate ${CONDA_ENV_NAME}"
	@ MESSAGE "- source .env"

pre-commit:
	@ pre-commit install -t pre-commit -t commit-msg
	@ SUCCESS "pre-commit set up"

lint: 
	@ ./build_steps/ci_pipeline/2_lint_code.sh

tests:
	@ ./build_steps/ci_pipeline/3_run_pytest.sh

# ----------------------------------------------------
#
# CD STEPS
#
# ----------------------------------------------------
.PHONY: image-latest image-tagged up check-services-health postgres-backup-test down publish-latest publish-tagged docker-deploy-tarball-custom run-ansible-playbook

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

helm-lint:
	@ ./deployment/kubernetes/scripts/lint_helm.sh

helm-test:
	@ ./deployment/kubernetes/scripts/test_helm.sh

helm-deploy:
	@ ./deployment/kubernetes/scripts/deploy_helm.sh

helm-generate-k8s-files:
	@ ./deployment/kubernetes/scripts/generate_helm_templates.sh

run-ansible-playbook:
	@ ./build_steps/cd_pipeline/9_run_ansible_playbooks.sh


# ----------------------------------------------------
#
# UTILS
#
# ----------------------------------------------------
# Ensure all environment variables are set
.PHONY: env-validation recreatedb
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
# check_defined = \
#     $(strip $(foreach 1,$1, \
#         $(call __check_defined,$1,$(strip $(value 2)))))
# __check_defined = \
#     $(if $(value $1),, \
#       $(error Undefined $1$(if $2, ($2))))

# $(call check_defined, CONDA_ENV_NAME, Please source .dev.env)
# $(call check_defined, S3_DOCKER_DEPLOY_TARBALL_CUSTOM, Please source .dev.env)
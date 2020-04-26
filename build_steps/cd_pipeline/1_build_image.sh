#!/bin/bash

# Usage:
# Build image with latest tag
#   .build_steps/cd_pipeline/1_build_image.sh
# Build image with project tag (pyproject.toml)
#   .build_steps/cd_pipeline/1_build_image.sh "tagged"

# Exit on error
set -e

# Set traps to clean up if exit or something goes wrong
trap "echo 'Something went wrong!' && exit 1" ERR

# Helper function: Exit with error
function exit_error() {
  ERROR "$1" 1>&2
  exit 1
}

function activate_environment() {
  source $(conda info --base)/etc/profile.d/conda.sh
  conda activate ${CONDA_ENV_NAME}
}

# Functions
function set_tag() {
  if [[ "$1" == "tagged" ]]; then
    TAG=$(poetry version | awk '{print $NF}')
  else
    TAG=latest
  fi
  if [[ -z $TAG ]]; then
    exit_error "TAG could not be set! Aborting."
  fi
}

function package_app() {
  INFO "Packaging portfolio app to /bin"
  python --version
  python utils/package_builder.py --name ${PROJECT_NAME}
  PACKAGE_APP_STATE=$?
  if [ "$PACKAGE_APP_STATE" -ne 0 ]; then
    exit_error "Packaging app failed! Aborting."
  fi
}

function build_image() {
  INFO "Building docker image ${IMAGE_REPOSITORY}:${TAG}"
  docker build -f ${DOCKERFILE_PATH} -t ${IMAGE_REPOSITORY}:${TAG} \
    --build-arg DOCKER_PORTFOLIO_HOME=${DOCKER_PORTFOLIO_HOME} \
    --build-arg DOCKER_APP_CODE=${DOCKER_APP_CODE} \
    --build-arg PORTFOLIO_TARBALL=./bin/portfolio.tar.gz . \
    --build-arg POETRY_VERSION=${POETRY_VERSION} \
    --build-arg POETRY_LOCK_FILE=./poetry.lock \
    --build-arg PYPROJECT_FILE=./pyproject.toml
  BUILD_IMAGE_STATE=$?
  if [ "$BUILD_IMAGE_STATE" -ne 0 ]; then
    exit_error "Build image failed! Aborting."
  fi
}

# Start script
activate_environment
set_tag $1
package_app
build_image
SUCCESS "${IMAGE_REPOSITORY}:${TAG} built successfully"
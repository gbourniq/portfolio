#!/bin/bash

# Usage:
# Push image with latest tag
#   .build_steps/cd_pipeline/3_push_docker_image.sh
# Push image with project tag (pyproject.toml)
#   .build_steps/cd_pipeline/3_push_docker_image.sh "tagged"

# Exit on error
set -e

# Set traps to clean up if exit or something goes wrong
trap "echo 'Something went wrong!' && exit 1" ERR

# Helper function: Exit with error
function exit_error() {
  ERROR "$1" 1>&2
  exit 1
}

function validate_environment_variables() {
  if [[ -z $DOCKER_PASSWORD ]] || \
     [[ -z $DOCKER_USER ]] || \
     [[ -z $CONDA_ENV_NAME ]] || \
     [[ -z $IMAGE_REPOSITORY ]]
  then
    exit_error "Some of the following environment variables are not set: \
DOCKER_PASSWORD, DOCKER_USER, CONDA_ENV_NAME, IMAGE_REPOSITORY. Aborting."
  fi
}

# Define functions
function docker_login() {
  if ! (echo "${DOCKER_PASSWORD}" | docker login --username "${DOCKER_USER}" --password-stdin 2>&1)
  then
    exit_error "Docker login failed! Aborting."
  fi
}

function activate_environment() {
  source $(conda info --base)/etc/profile.d/conda.sh
  conda activate ${CONDA_ENV_NAME}
}

function set_tag() {
  if [[ "$1" == "tagged" ]]; then
    activate_environment
    TAG=$(poetry version | awk '{print $NF}')
  else
    TAG=latest
  fi
  if [[ -z $TAG ]]; then
    exit_error "TAG could not be set! Aborting."
  fi
}

function push_image() {
  INFO "Publishing ${IMAGE_REPOSITORY}:${TAG} image to ${DOCKER_REGISTRY:-docker.io}..."
  if ! (docker push ${IMAGE_REPOSITORY}:${TAG})
  then
    exit_error "Pushing ${IMAGE_REPOSITORY}:${TAG} failed! Aborting."
  else
    SUCCESS "${IMAGE_REPOSITORY}:${TAG} published successfully!"
  fi
}


# Start script
validate_environment_variables
docker_login
set_tag $1
push_image
docker logout
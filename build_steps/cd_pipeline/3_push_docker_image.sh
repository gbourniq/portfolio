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

# Define functions
function docker_login() {
  echo "${DOCKER_PASSWORD}" | docker login --username "${DOCKER_USER}" --password-stdin 2>&1
  DOCKER_LOGIN_STATE=$?
  if [ "$DOCKER_LOGIN_STATE" -ne 0 ]; then
    exit_error "Docker login failed! Aborting."
  fi
}

set_tag() {
  if [[ $1 == tagged ]]; then
    source $(conda info --base)/etc/profile.d/conda.sh
    conda activate ${CONDA_ENV_NAME}
    TAG=$(poetry version | awk '{print $NF}')
  else
    TAG=latest
  fi
  if [[ -z $TAG ]]; then
    exit_error "TAG could not be set! Aborting."
  fi
}

function push_image() {
  INFO "Publishing ${IMAGE_REPOSITORY}:latest image to ${DOCKER_REGISTRY:-docker.io}..."
  docker push ${IMAGE_REPOSITORY}:latest
  PUBLISH_STATE=$?
  if [ "$PUBLISH_STATE" -ne 0 ]; then
    exit_error "Pushing ${IMAGE_REPOSITORY}:latest failed! Aborting."
  else
    SUCCESS "${IMAGE_REPOSITORY}:latest published successfully!"
  fi
}

# Start script
docker_login
set_tag $1
push_image
docker logout
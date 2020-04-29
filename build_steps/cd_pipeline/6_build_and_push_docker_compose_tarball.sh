#!/bin/bash

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


INFO "Setting PYTHONPATH to $PWD for tarball script imports to work properly"
export PYTHONPATH=$PWD

INFO "Build docker_deploy.tar.gz"
activate_environment
python utils/build_docker_deploy_tarball.py
BUILD_SCRIPT_STATE=$?
if [ "$BUILD_SCRIPT_STATE" -ne 0 ]; then
  exit_error "Build script failed! Aborting."
fi

INFO "Upload docker_deploy.tar.gz to S3"
aws s3 cp ./bin/docker_deploy.tar.gz ${S3_DOCKER_DEPLOY_URI}/
S3_UPLOAD_STATE=$?
if [ "$S3_UPLOAD_STATE" -ne 0 ]; then
  exit_error "S3 upload failed! Aborting."
fi

SUCCESS "docker_deploy.tar.gz built and uploaded to S3."
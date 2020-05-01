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

s3_uri=$1
# If not argument given, set ${S3_DOCKER_DEPLOY_URI_DEV} as default URI
if [[ -z $s3_uri ]]; then
  s3_uri=${S3_DOCKER_DEPLOY_URI_DEV}
fi

docker_deploy_tarball_name=$2
# If not argument given, set 'docker_deploy' as default tarball name
if [[ -z $docker_deploy_tarball_name ]]; then
  docker_deploy_tarball_name=docker_deploy
fi

INFO "Setting PYTHONPATH to $PWD for tarball script imports to work properly"
export PYTHONPATH=$PWD

INFO "Build docker deploy tarball"
activate_environment
python utils/build_docker_deploy_tarball.py --name ${docker_deploy_tarball_name}
BUILD_SCRIPT_STATE=$?
if [ "$BUILD_SCRIPT_STATE" -ne 0 ]; then
  exit_error "Build script failed! Aborting."
fi

INFO "Upload docker deploy tarball to S3"
aws s3 cp ./bin/${docker_deploy_tarball_name}.tar.gz ${s3_uri}/
S3_UPLOAD_STATE=$?
if [ "$S3_UPLOAD_STATE" -ne 0 ]; then
  exit_error "Oops.. S3 upload to ${s3_uri} has failed! Aborting."
fi

SUCCESS "${docker_deploy_tarball_name}.tar.gz successfully built and uploaded to S3."
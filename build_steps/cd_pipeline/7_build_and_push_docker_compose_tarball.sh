#!/bin/bash

# Exit on error
set -e

# Set traps to clean up if exit or something goes wrong
trap "echo 'Something went wrong!' && exit 1" ERR

# Retrieve arguments
s3_uri=${S3_DOCKER_DEPLOY_URI}
docker_deploy_tarball_name=$1

# If not argument given, use 'docker_deploy_cd_pipeline.tar.gz' as default tarball name
if [[ -z $docker_deploy_tarball_name ]]; then
  docker_deploy_tarball_name=${S3_DOCKER_DEPLOY_TARBALL_CD_PIPELINE}
fi

# Functions
function exit_error() {
  ERROR "$1" 1>&2
  exit 1
}

function activate_environment() {
  source $(conda info --base)/etc/profile.d/conda.sh
  conda activate ${CONDA_ENV_NAME}
}

function validate_environment_variables() {
  if [[ -z $S3_DOCKER_DEPLOY_URI ]] || \
     [[ -z $S3_DOCKER_DEPLOY_TARBALL_CD_PIPELINE ]] || \
     [[ -z $CONDA_ENV_NAME ]]
  then
    exit_error "Some of the following environment variables are not set: \
CONDA_ENV_NAME, S3_DOCKER_DEPLOY_URI, S3_DOCKER_DEPLOY_TARBALL_CD_PIPELINE. Aborting."
  fi
}


# Start script
validate_environment_variables

INFO "Setting PYTHONPATH to $PWD for tarball script imports to work properly"
export PYTHONPATH=$PWD

INFO "Building docker deploy tarball..."
activate_environment
if ! (python utils/build_docker_deploy_tarball.py --name ${docker_deploy_tarball_name})
then
  exit_error "Build script failed! Aborting."
else
  SUCCESS "${docker_deploy_tarball_name}.tar.gz successfully built and located in bin/"
fi

if [[ $AWS_ENABLED != True ]]; then
  INFO "AWS_ENABLED not set to True. docker deploy tarball will not be uploaded to S3."
  exit 0
else
  INFO "Uploading docker deploy tarball to S3..."
fi

if ! (aws s3 cp ./bin/${docker_deploy_tarball_name}.tar.gz ${s3_uri}/)
then
  exit_error "Oops.. S3 upload to ${s3_uri} has failed! Aborting."
fi

SUCCESS "${docker_deploy_tarball_name}.tar.gz successfully built and uploaded to S3."
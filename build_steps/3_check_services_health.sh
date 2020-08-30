#!/bin/bash

# Exit on error
set -e

# Set traps to clean up if exit or something goes wrong
trap "echo 'Something went wrong! Tidying up...' && remove_services && exit 1" ERR

# Helper function: Exit with error
function exit_error() {
  ERROR "$1" 1>&2
  exit 1
}

cd deployment/docker-deployment
source ../../scripts/check_services_health.sh
cd -

if [[ ${deployment_unhealthy:?} == True ]]; then
  exit_error "Unhealthy deployment! Aborting."
fi

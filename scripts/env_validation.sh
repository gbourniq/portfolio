#!/bin/bash

# Exit on error
set -e

# Set traps to clean up if exit or something goes wrong
trap "echo 'Something went wrong! Tidying up...' && exit 1" ERR

# Helper function: Exit with error
function exit_error() {
  ERROR "$1" 1>&2
  exit 1
}

# Sensitive variables to be defined on local host, eg. ~/.bash_profile
# and in the Travis CI Configuration Build
if [[ -z $DOCKER_PASSWORD ]]; then
    exit_error "DOCKER_PASSWORD environment variable required to run"
fi
if [[ -z $AWS_ACCESS_KEY_ID ]]; then
    exit_error "AWS_ACCESS_KEY_ID environment variable required to run"
fi
if [[ -z $AWS_SECRET_ACCESS_KEY ]]; then
    exit_error "AWS_SECRET_ACCESS_KEY environment variable required to run"
fi
if [[ -z $ANSIBLE_VAULT_PASSWORD ]]; then
    exit_error "ANSIBLE_VAULT_PASSWORD environment variable required to run"
fi
if [[ -z $ANSIBLE_SSH_PASSWORD ]]; then
    exit_error "ANSIBLE_SSH_PASSWORD environment variable required to run"
fi

SUCCESS All required environment variables are set
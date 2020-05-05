##!/bin/bash

set -e

# Set traps to clean up if exit or something goes wrong
trap "echo 'Something went wrong! && exit 1" ERR

# Helper function: Exit with error
function exit_error() {
  ERROR "$1" 1>&2
  exit 1
}

function activate_environment() {
  INFO "Activating ${CONDA_ENV_NAME} conda environment"
  source $(conda info --base)/etc/profile.d/conda.sh
  conda activate ${CONDA_ENV_NAME}
}

if [[ -z $CONDA_ENV_NAME ]]; then
  exit_error "CONDA_ENV_NAME not set! Aborting."
fi

activate_environment
INFO "Running pre-commit to lint code"
if ! (pre-commit run --all-files)
then
    exit_error "Some code linting have failed! Aborting."
else
    SUCCESS "Code linted successfully" 
fi
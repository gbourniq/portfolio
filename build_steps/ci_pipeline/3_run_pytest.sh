#!/bin/bash

set -e

# Set traps to clean up if exit or something goes wrong
trap "echo 'Something went wrong! && exit 1" ERR

# Helper function: Exit with error
function exit_error() {
  ERROR "$1" 1>&2
  exit 1
}

function activate_environment() {
  source $(conda info --base)/etc/profile.d/conda.sh
  conda activate ${CONDA_ENV_NAME}
}

if [[ -z $CONDA_ENV_NAME ]]; then
  exit_error "CONDA_ENV_NAME not set! Aborting."
fi

activate_environment
INFO "Run tests in pytest" 
cd app/
pytest -vvx

if [ $? -ne 0 ]; then
    exit_error "Some tests have failed! Aborting."
else
    SUCCESS "Run tests in pytest" 
fi
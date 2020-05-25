#!/bin/bash

set -e

# Set traps to clean up if exit or something goes wrong
trap "echo 'Something went wrong! && exit 1" ERR

# Helper function: Exit with error
function exit_error() {
  ERROR "$1" 1>&2
  cd -
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
INFO "Run tests with pytest-django" 
cd app/


INFO "Temporarily overriding MEDIA_URL, POSTGRES_HOST, and REDIS_HOST for tests (pytest.ini)"

if ! (pytest --cov=. --cov-report=term-missing); then
  exit_error "Some tests have failed! Aborting."
fi

SUCCESS "Run tests successfully with pytest-django" 
cd -
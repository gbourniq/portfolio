#!/bin/bash

# Exit on error
set -e

# Set traps to clean up if exit or something goes wrong
trap "echo 'Something went wrong! Tidying up...' && tidy_up && exit 1" ERR

# Helper function: Exit with error
function exit_error() {
  ERROR "$1" 1>&2
  exit 1
}

# Helper function: Exit with error
function tidy_up() {
  INFO "Removing ${CONDA_ENV_NAME} conda environment"
  source $(conda info --base)/etc/profile.d/conda.sh || true
  conda deactivate || true
  conda remove -y -n ${CONDA_ENV_NAME} --all || true
}

# Functions
function create_conda_env() {
  INFO "Creating ${CONDA_ENV_NAME} conda environment"
  conda env create
}

function activate_conda_env() {
  INFO "Activating ${CONDA_ENV_NAME} conda environment"
  source $(conda info --base)/etc/profile.d/conda.sh
  conda activate ${CONDA_ENV_NAME}
  if [ $? -ne 0 ]; then
    exit_error "conda activate failed! Aborting."
  fi
}

function run_poetry_install() {
  INFO "Installing Poetry dependencies"
  poetry install
  if [ $? -ne 0 ]; then
    exit_error "poetry installed failed! Aborting."
  fi
}


if [[ -z $CONDA_ENV_NAME ]]; then
  exit_error "CONDA_ENV_NAME not set! Aborting."
fi

# Start scripts
tidy_up
create_conda_env
activate_conda_env
run_poetry_install
SUCCESS "Environment set up successfully!"


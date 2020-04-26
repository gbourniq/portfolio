##!/bin/bash

set -e

# Set traps to clean up if exit or something goes wrong
trap "echo 'Something went wrong! && exit 1" ERR

# Helper function: Exit with error
function exit_error() {
  ERROR "$1" 1>&2
  exit 1
}

INFO "Activating ${CONDA_ENV_NAME} conda environment"
source $(conda info --base)/etc/profile.d/conda.sh
conda activate ${CONDA_ENV_NAME}

INFO "Running pre-commit to lint code"
pre-commit run --all-files

OUTPUT_CODE=$?
if [ $OUTPUT_CODE -ne 0 ]; then
    exit_error "Some code linting have failed! Aborting."
else
    SUCCESS "Code linted successfully" 
fi
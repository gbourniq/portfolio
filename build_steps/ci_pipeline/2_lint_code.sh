##!/bin/bash

set -e

INFO "Activating ${CONDA_ENV_NAME} conda environment"
source $(conda info --base)/etc/profile.d/conda.sh
conda activate ${CONDA_ENV_NAME}

INFO "Running pre-commit to lint code"
pre-commit run --all-files

OUTPUT_CODE=$?
if [ $OUTPUT_CODE -ne 0 ]; then
    WARNING "Some code linting have failed! Aborting CI pipeline."
else
    SUCCESS "Code linted successfully" 
fi
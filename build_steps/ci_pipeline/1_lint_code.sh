##!/bin/bash

set -e


INFO "Activating ${CONDA_ENV_NAME} conda environment"
source $$(conda info --base)/etc/profile.d/conda.sh
conda activate ${CONDA_ENV_NAME}

INFO "Running pre-commit to lint code"
pre-commit run --all-files
SUCCESS "Code linted successfully"
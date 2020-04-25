#!/bin/bash

INFO "Creating ${CONDA_ENV_NAME} conda environment"
conda env create

INFO "Activating ${CONDA_ENV_NAME} conda environment"
source $(conda info --base)/etc/profile.d/conda.sh
conda activate ${CONDA_ENV_NAME}

INFO "Installing Poetry dependencies"
poetry install

SUCCESS "Environment set up successfully!"


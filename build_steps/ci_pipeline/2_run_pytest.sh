#!/bin/bash

INFO "Activating ${CONDA_ENV_NAME} conda environment"
source $$(conda info --base)/etc/profile.d/conda.sh
conda activate ${CONDA_ENV_NAME}

INFO "Run tests in pytest" 
cd app/
pytest -vvx

OUTPUT_CODE=$?
if [ $OUTPUT_CODE -ne 0 ]; then
    WARNING "Some tests have failed! Aborting CI pipeline."
else
    SUCCESS "Run tests in pytest" 
fi
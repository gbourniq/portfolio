#!/bin/bash

set -e

# Source environment variable for dev build
source ./.dev.env

# Validate secret environment variables are set
if [[ $VALIDATION_FAILED == True ]]; then
    exit 1
fi

CI_PIPELINE_DIR="build_steps/ci_pipeline"

for entry in "$CI_PIPELINE_DIR"/*
do
  source "$entry"
done
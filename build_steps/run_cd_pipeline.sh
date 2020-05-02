#!/bin/bash

set -e

# Source environment variable for dev build
source ./.dev.env

# Validate secret environment variables are set
if [[ $VALIDATION_FAILED == True ]]; then
    exit 1
fi

CD_PIPELINE_DIR="build_steps/cd_pipeline"

for entry in "$CD_PIPELINE_DIR"/*
do
  source "$entry"
done
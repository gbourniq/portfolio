#!/bin/bash

set -e

source ./scripts/env_validation.sh

if [[ $VALIDATION_FAILED == True ]]; then
    exit 1
fi

CD_PIPELINE_DIR="build_steps/cd_pipeline"

for entry in "$CD_PIPELINE_DIR"/*
do
  source "$entry"
done
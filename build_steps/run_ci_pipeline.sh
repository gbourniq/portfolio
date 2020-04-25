#!/bin/bash

CI_PIPELINE_DIR="build_steps/ci_pipeline"

for entry in "$CI_PIPELINE_DIR"/*
do
  source "$entry"
done
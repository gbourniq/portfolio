#!/bin/bash

CD_PIPELINE_DIR="build_steps/cd_pipeline"

for entry in "$CD_PIPELINE_DIR"/*
do
  source "$entry"
done
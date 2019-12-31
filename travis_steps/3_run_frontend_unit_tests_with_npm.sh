#!/bin/bash

set -xe #  exit as soon as any command returns a nonzero status

# Activate env for the compatible NodeJs version
# source $CONDA_BIN/activate devops-test

# Install node modules
# We want to make sure we’re doing a clean install of our dependencies
# npm ci

# By default the test script runs the tests in watch mode.
# In this build we have set environment variable CI=true, so it can return 0/1 code.
# npm run test:ci
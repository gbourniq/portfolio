#!/bin/bash

set -xe #  exit as soon as any command returns a nonzero status

# Activate env

# Run tests in pytest
echo 'Running pytest'
# pytest -vvx --cov=
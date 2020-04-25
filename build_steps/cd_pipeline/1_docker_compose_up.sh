#!/bin/bash

# echo "Using $prefix as prefix for installer artifacts"
# prefix="bin/installer"

# echo "Getting the cpip and it's dependencies..."
# source build_steps/utils/activate_cpip.sh

# echo "Clearing any existing $prefix existence to make way for installers"
# rm -rf $prefix

# echo "Creating MVP installer artifacts"
# ./package/create-installer-artifacts -p $prefix

  - export BUILD=dev && make up && make down
  - export BUILD=prod && make up && make down
#!/bin/bash

# echo "Using $prefix as prefix for installer artifacts"
# prefix="bin/installer"

# echo "Getting the cpip and it's dependencies..."
# source build_steps/utils/activate_cpip.sh

# echo "Clearing any existing $prefix existence to make way for installers"
# rm -rf $prefix

# echo "Creating MVP installer artifacts"
# ./package/create-installer-artifacts -p $prefix

  - make portfolio
  - make latest
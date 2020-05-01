#!/bin/bash

# Helper function: Exit with error
function set_as_failed() {
  MESSAGE "$1" 1>&2
  VALIDATION_FAILED=True
}

# Required environment for development
function env_check_dev() {
    if [[ -z $DOCKER_USER ]]; then
        set_as_failed "DOCKER_USER environment variable required to run"
    fi
    if [[ -z $DOCKER_PASSWORD ]]; then
        set_as_failed "DOCKER_PASSWORD environment variable required to run"
    fi
    if [[ -z $AWS_ACCESS_KEY_ID ]]; then
        set_as_failed "AWS_ACCESS_KEY_ID environment variable required to run"
    fi
    if [[ -z $AWS_SECRET_ACCESS_KEY ]]; then
        set_as_failed "AWS_SECRET_ACCESS_KEY environment variable required to run"
    fi
    if [[ -z $ANSIBLE_VAULT_PASSWORD ]] && [[ $RUN_ANSIBLE_PLAYBOOK == True ]]; then
        set_as_failed "ANSIBLE_VAULT_PASSWORD not set, but RUN_ANSIBLE_PLAYBOOK=True! Aborting."
    fi
    if [[ -z $ANSIBLE_SSH_PASSWORD ]] && [[ $RUN_ANSIBLE_PLAYBOOK == True ]]; then
        set_as_failed "ANSIBLE_SSH_PASSWORD not set, but RUN_ANSIBLE_PLAYBOOK=True! Aborting."
    fi
}

# Required environment for production
function env_check_prod() {
    if [[ -z $AWS_ACCESS_KEY_ID ]]; then
        set_as_failed "AWS_ACCESS_KEY_ID environment variable required to run"
    fi
    if [[ -z $AWS_SECRET_ACCESS_KEY ]]; then
        set_as_failed "AWS_SECRET_ACCESS_KEY environment variable required to run"
    fi
}

# Validate environment variables are set
function validate_env() {
    if [[ -z $BUILD ]]; then
        set_as_failed "BUILD environment variable not set. Please source .env! Aborting."
    elif [[ $BUILD == dev ]]; then
        env_check_dev
    elif [[ $BUILD == prod ]]; then
        env_check_prod
    else
        set_as_failed "Unknown build type: ${BUILD}. Expected either dev or prod! Aborting."
    fi
}

# Validate custom bash functions are set
function validate_functions() {
    functions=(INFO MESSAGE SUCCESS ERROR)
    for function_name in ${functions[*]}; do
        if [[ $(declare -f ${function_name} > /dev/null; echo $?) -ne 0 ]]; then
            set_as_failed "function ${function_name} not defined"
        fi
    done
}

# Start script
VALIDATION_FAILED=False
validate_env
validate_functions

# Success message if set_as_failed() not called
if [[ $BUILD == prod ]] && [[ $VALIDATION_FAILED != True ]]; then
    SUCCESS "Environment variables are all set for production build!"
elif [[ $BUILD == dev ]] && [[ $VALIDATION_FAILED != True ]]; then
    SUCCESS "Environment variables are all set for development build!"
else
    ERROR "Oops.. Environment validation has failed!"
fi
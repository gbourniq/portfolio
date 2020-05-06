#!/bin/bash

# Helper function: Exit with error
function set_as_failed() {
  ERROR "$1" 1>&2
  VALIDATION_FAILED=True
}

# Required environment for development
function secret_env_check_dev() {
    if [[ ! $DOCKER_USER || ! $DOCKER_PASSWORD ]]; then
        set_as_failed "DOCKER_USER and DOCKER_PASSWORD environment variables are not set!"
    fi
    if [[ ! $AWS_ACCESS_KEY_ID && $AWS_ENABLED == True ]]; then
        set_as_failed "AWS_ACCESS_KEY_ID not set, but AWS_ENABLED=True!"
    fi
    if [[ ! $AWS_SECRET_ACCESS_KEY && $AWS_ENABLED == True ]]; then
        set_as_failed "AWS_SECRET_ACCESS_KEY, but AWS_ENABLED=True!"
    fi
    if [[ ! $ANSIBLE_VAULT_PASSWORD && $RUN_ANSIBLE_PLAYBOOK == True ]]; then
        set_as_failed "ANSIBLE_VAULT_PASSWORD not set, but RUN_ANSIBLE_PLAYBOOK=True!"
    fi
    if [[ ! $ANSIBLE_SSH_PASSWORD && $RUN_ANSIBLE_PLAYBOOK == True ]]; then
        set_as_failed "ANSIBLE_SSH_PASSWORD not set, but RUN_ANSIBLE_PLAYBOOK=True!"
    fi
}

# Required environment for production
function secret_env_check_prod() {
    if [[ ! $AWS_ACCESS_KEY_ID && $AWS_ENABLED == True ]]; then
        set_as_failed "AWS_ACCESS_KEY_ID not set, but AWS_ENABLED=True!"
    fi
    if [[ ! $AWS_SECRET_ACCESS_KEY && $AWS_ENABLED == True ]]; then
        set_as_failed "AWS_SECRET_ACCESS_KEY, but AWS_ENABLED=True!"
    fi
}

# Validate environment variables are set
function validate_env() {
    if [[ ! $BUILD ]]; then
        set_as_failed "BUILD environment variable not set. Please source .env!"
    elif [[ $BUILD == dev ]]; then
        secret_env_check_dev
    elif [[ $BUILD == prod ]]; then
        secret_env_check_prod
    else
        set_as_failed "Unknown build type: ${BUILD}. Expected either dev or prod!"
    fi
}

# Validate custom bash functions are set
function validate_functions() {
    functions=(INFO MESSAGE SUCCESS ERROR)
    for function_name in ${functions[*]}; do
        if ! (declare -f ${function_name} > /dev/null)
        then
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
    MESSAGE "✅ [PROD build] Secret environment variables are all set!"
elif [[ $BUILD == dev ]] && [[ $VALIDATION_FAILED != True ]]; then
    MESSAGE "✅ [DEV build] Secret environment variables are all set!"
else
    ERROR "❌ Oops.. Environment validation has failed!"
fi
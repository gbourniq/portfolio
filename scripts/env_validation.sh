#!/bin/bash

# Helper function: Exit with error
function set_as_failed() {
  ERROR "$1" 1>&2
  VALIDATION_FAILED=True
}

# Required environment variables for dev build
# function secret_env_check_dev() {
#     if [[ $RUN_ANSIBLE_PLAYBOOK == True && ! $AWS_ACCESS_KEY_ID || ! $AWS_SECRET_ACCESS_KEY ]]; then
#         set_as_failed "Please set both AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY, or set RUN_ANSIBLE_PLAYBOOK to False"
#     fi
# }

# Required environment for docker compose up
function validate_docker_compose_env() {
    if [[ ! $DOCKER_PORTFOLIO_HOME ]]; then
        set_as_failed "DOCKER_PORTFOLIO_HOME not set"
    fi
    if [[ ! $SECRET_KEY ]]; then
        set_as_failed "SECRET_KEY not set"
    fi
    if [[ ! $LOGGING_ENABLED ]]; then
        set_as_failed "LOGGING_ENABLED not set"
    fi
    if [[ ! $POSTGRES_DB || ! $POSTGRES_USER || ! $POSTGRES_PASSWORD || ! $POSTGRES_HOST || ! $POSTGRES_PORT ]]; then
        set_as_failed "POSTGRES_DB not set"
    fi
    if [[ ! $REDIS_HOST || ! $REDIS_HOST ]]; then
        set_as_failed "REDIS_HOST and REDIS_HOST not set"
    fi
    if [[ ! $EMAIL_HOST_USER || ! $EMAIL_HOST_PASSWORD ]]; then
        INFO "WARNING: Django EMAIL_HOST_USER not set"
    fi
    if [[ ! $AWS_STORAGE_BUCKET_NAME ]]; then
        set_as_failed "AWS_STORAGE_BUCKET_NAME not set"
    fi
    if [[ ! $AWS_DEFAULT_REGION ]]; then
        set_as_failed "AWS_DEFAULT_REGION not set"
    fi
}

# Validate environment variables are set
function validate_env() {
    if [[ ! $BUILD ]]; then
        set_as_failed "BUILD environment variable not set. Please source .env!"
    elif [[ $BUILD == dev ]]; then
        # secret_env_check_dev
        MESSAGE "dev mode!"
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
if [[ $BUILD == prod ]]; then
    validate_docker_compose_env
    INFO "Loaded Django settings for production environment"
    INFO "Docker deployment: make up"
elif [[ $BUILD == dev ]]; then
    INFO "Loaded Django settings for development environment"
    INFO "Baremetal deployment: cd app && python manage.py runserver"
    INFO "Docker deployment: make image-latest && make up"
fi

# Success message if set_as_failed() not called
if [[ $BUILD == prod ]] && [[ $VALIDATION_FAILED != True ]]; then
    SUCCESS "[[BUILD=prod] Secret environment variables are all set!"
elif [[ $BUILD == dev ]] && [[ $VALIDATION_FAILED != True ]]; then
    SUCCESS "[BUILD=dev] Secret environment variables are all set!"
else
    ERROR "BUILD=$BUILD, VALIDATION_FAILED=$VALIDATION_FAILED - Oops.. Environment validation has failed!"
fi
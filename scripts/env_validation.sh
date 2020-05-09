#!/bin/bash

# Helper function: Exit with error
function set_as_failed() {
  ERROR "$1" 1>&2
  VALIDATION_FAILED=True
}

# Required environment variables for dev build
function secret_env_check_dev() {
    if [[ ! $DOCKER_USER || ! $DOCKER_PASSWORD ]]; then
        set_as_failed "DOCKER_USER and DOCKER_PASSWORD environment variables are not set!"
    fi
    if [[ ! $AWS_ACCESS_KEY_ID && $AWS_ENABLED == True ]]; then
        set_as_failed "AWS_ACCESS_KEY_ID not set, but AWS_ENABLED=True!"
    fi
    if [[ ! $AWS_SECRET_ACCESS_KEY && $AWS_ENABLED == True ]]; then
        set_as_failed "AWS_SECRET_ACCESS_KEY not set, but AWS_ENABLED=True!"
    fi
    if [[ $RUN_ANSIBLE_PLAYBOOK == True && $AWS_ENABLED != True ]]; then
        set_as_failed "If RUN_ANSIBLE_PLAYBOOK set to True, then AWS_ENABLED must also be to True"
    fi
    if [[ ! $ANSIBLE_VAULT_PASSWORD && $RUN_ANSIBLE_PLAYBOOK == True ]]; then
        set_as_failed "ANSIBLE_VAULT_PASSWORD not set, but RUN_ANSIBLE_PLAYBOOK=True!"
    fi
    if [[ ! $ANSIBLE_SSH_PASSWORD && $RUN_ANSIBLE_PLAYBOOK == True ]]; then
        set_as_failed "ANSIBLE_SSH_PASSWORD not set, but RUN_ANSIBLE_PLAYBOOK=True!"
    fi
}

# Required environment variables for prod build
function secret_env_check_prod() {
    if [[ ! $AWS_ACCESS_KEY_ID && $AWS_ENABLED == True ]]; then
        set_as_failed "AWS_ACCESS_KEY_ID not set, but AWS_ENABLED=True!"
    fi
    if [[ ! $AWS_SECRET_ACCESS_KEY && $AWS_ENABLED == True ]]; then
        set_as_failed "AWS_SECRET_ACCESS_KEY, but AWS_ENABLED=True!"
    fi
}

# Required environment for docker compose up
function validate_docker_compose_env() {
    if [[ ! $DOCKER_PORTFOLIO_HOME ]]; then
        set_as_failed "DOCKER_PORTFOLIO_HOME not set"
    fi
    if [[ ! $DEBUG ]]; then
        set_as_failed "DEBUG not set"
    fi
    if [[ ! $ALLOWED_HOSTS ]]; then
        set_as_failed "ALLOWED_HOSTS not set"
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
    if [[ ! $EMAIL_HOST_USER || ! $EMAIL_HOST_USER ]]; then
        set_as_failed "EMAIL_HOST_USER and EMAIL_HOST_USER not set"
    fi
    if [[ ! $ENABLE_S3_FOR_DJANGO_FILES ]]; then
        set_as_failed "ENABLE_S3_FOR_DJANGO_FILES not set"
    fi
    if [[ ! $AWS_STORAGE_BUCKET_NAME ]]; then
        set_as_failed "AWS_STORAGE_BUCKET_NAME not set"
    fi
    if [[ ! $AWS_DEFAULT_REGION ]]; then
        set_as_failed "AWS_DEFAULT_REGION not set"
    fi
    if [[ ! $AWS_ACCESS_KEY_ID || ! $AWS_SECRET_ACCESS_KEY ]]; then
        set_as_failed "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY not set"
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
if [[ $BAREMETAL_DEPLOYMENT == False ]]; then
    validate_docker_compose_env
fi

# Success message if set_as_failed() not called
if [[ $BUILD == prod ]] && [[ $VALIDATION_FAILED != True ]]; then
    MESSAGE "✅ [PROD build] Secret environment variables are all set!"
elif [[ $BUILD == dev ]] && [[ $VALIDATION_FAILED != True ]]; then
    MESSAGE "✅ [DEV build] Secret environment variables are all set!"
else
    ERROR "❌ Oops.. Environment validation has failed!"
fi
#!/bin/bash

# Exit on error
set -e

# Set exit trap
trap "echo 'Exiting script...' && exit_handler" EXIT

function exit_handler() {
  if [ $playbook_success == True ]; then
    exit 0
  else
    ERROR "Ansible playbook failed. Aborting!" 1>&2
    tidy_up
    exit 1
  fi
}

function tidy_up() {
  MESSAGE "Tidying up..."
  ansible-playbook stop_instance.yml -vv
}

function activate_environment() {
  source $(conda info --base)/etc/profile.d/conda.sh
  conda activate ${CONDA_ENV_NAME}
}

function validate_environment_variables() {
  if [[ -z $RUN_ANSIBLE_PLAYBOOK || -z $CONDA_ENV_NAME ]]
  then
    exit_error "Some of the following environment variables are not set: \
RUN_ANSIBLE_PLAYBOOK, CONDA_ENV_NAME. Aborting."
  fi
}

function set_ansible_vault() {
  echo "${ANSIBLE_VAULT_PASSWORD}" > /tmp/ansible-vault-pw
}

function run_qa_playbook() {
    ansible-playbook docker_deployment.yml -vvv
}


# Start script
if [ "$RUN_ANSIBLE_PLAYBOOK" != True ]; then
  INFO "RUN_ANSIBLE_PLAYBOOK is not set to True. Aborting."
  playbook_success=True
  exit 0
fi
validate_environment_variables
activate_environment
INFO "Run the Ansible QA playbook..."
cd ansible
set_ansible_vault
playbook_success=False
run_qa_playbook
playbook_success=True
SUCCESS "QA playbook was run successfully!"







#!/bin/bash

# Exit on error
set -e

# Set exit trap
trap "echo 'Exiting script...' && exit_handler" EXIT

function exit_handler() {
  if [ $playbook_success == True ]; then
    SUCCESS "QA playbook was run successfully!"
    tidy_up
    exit 0
  else
    ERROR "Ansible playbook failed. Aborting!" 1>&2
    tidy_up
    exit 1
  fi
}

function tidy_up() {
  MESSAGE "Tidying up..."
  ansible-playbook \
    -i inventories \
    --vault-id /tmp/ansible-vault-pw \
    stop_instance.yml \
    -vv
  rm -rf /tmp/ansible-vault-pw
}

function activate_environment() {
  source $(conda info --base)/etc/profile.d/conda.sh
  conda activate ${CONDA_ENV_NAME}
}

function validate_environment_variables() {
  if [[ -z $RUN_ANSIBLE_PLAYBOOK ]] || \
     [[ -z $CONDA_ENV_NAME ]]
  then
    exit_error "Some of the following environment variables are not set: \
RUN_ANSIBLE_PLAYBOOK, CONDA_ENV_NAME. Aborting."
  fi
}

function set_ansible_vault() {
  echo "${ANSIBLE_VAULT_PASSWORD}" > /tmp/ansible-vault-pw
}

function run_qa_playbook() {
  ansible-playbook \
    -i inventories \
    --vault-id /tmp/ansible-vault-pw \
    docker_deployment.yml \
		--skip-tags="stop-instance" \
    -vv
}


# Start script
validate_environment_variables
if [ "$RUN_ANSIBLE_PLAYBOOK" == True ]; then
  activate_environment
  INFO "Run the Ansible QA playbook..."
  cd ansible
  set_ansible_vault
  playbook_success=False
  run_qa_playbook
  playbook_success=True
else
  INFO "RUN_ANSIBLE_PLAYBOOK is set to False. Aborting."
  exit 0
fi









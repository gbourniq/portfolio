#!/bin/bash

# Exit on error
set -e

# Set exit trap
trap "echo 'Exiting script...' && exit_handler" EXIT

function exit_handler() {
  if [ $playbook_success == True ]; then
    tidy_up
    exit 0
  elif [ $playbook_success == False ]; then
    ERROR "Ansible playbook failed. Aborting!" 1>&2
    tidy_up
    exit 1
  else
    MESSAGE "Clean exit."
    exit 0
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
  if [[ -z $RUN_ANSIBLE_PLAYBOOK || -z $CONDA_ENV_NAME || -z $ANSIBLE_VAULT_PASSWORD ]]
  then
    exit_error "Some of the following environment variables are not set: \
RUN_ANSIBLE_PLAYBOOK, CONDA_ENV_NAME, ANSIBLE_VAULT_PASSWORD. Aborting."
  fi
}

function set_ansible_vault() {
  echo "${ANSIBLE_VAULT_PASSWORD}" > /tmp/ansible-vault-pw
}

function run_qa_playbook() {
  if [[ $ENABLE_SLACK_NOTIFICATION == True ]]; then
    ansible-playbook \
      -i inventories \
      --vault-id /tmp/ansible-vault-pw \
      docker_deployment.yml \
      -vvv
  else
    ansible-playbook \
      -i inventories \
      --vault-id /tmp/ansible-vault-pw \
      docker_deployment.yml \
      --skip-tags="slack-notification" \
      -vv
  fi
}


# Start script
if [ "$RUN_ANSIBLE_PLAYBOOK" != True ]; then
  INFO "RUN_ANSIBLE_PLAYBOOK is not set to True. Aborting."
  playbook_success=ExitNoTidyUp
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







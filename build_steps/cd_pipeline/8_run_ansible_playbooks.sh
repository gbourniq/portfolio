#!/bin/bash

# Exit on error
set -e

# Set traps to clean up if exit or something goes wrong
trap "echo 'Something went wrong! Tidying up...' && tidy_up && exit 1" ERR
trap "echo 'Tidying up...' && tidy_up && exit 0" EXIT

# Helper function: Exit with error
function exit_error() {
  ERROR "$1" 1>&2
  exit 1
}

# Define functions
function tidy_up() {
  rm -rf /tmp/ansible-vault-pw
  exit 0
}

function set_ansible_vault() {
  echo "${ANSIBLE_VAULT_PASSWORD}" > /tmp/ansible-vault-pw
}

function run_qa_playbook() {

  ansible-playbook \
    -i inventories \
    --vault-id /tmp/ansible-vault-pw \
    site.yml \
    --skip-tags="slack-notification-dev" \
    -vv

    ANSIBLE_OUTPUT_STATE=$?
    if [ "$ANSIBLE_OUTPUT_STATE" -ne 0 ]; then
      exit_error "Ansible playbook failed! Aborting."
    fi
}


# Start script
if [ "$RUN_ANSIBLE_PLAYBOOK" == True ]; then
  INFO "Run the Ansible QA playbook..."
  cd ansible
  set_ansible_vault
  run_qa_playbook
  SUCCESS "QA playbook was run successfully!"
else
  INFO "RUN_ANSIBLE_PLAYBOOK is set to False. Aborting."
fi









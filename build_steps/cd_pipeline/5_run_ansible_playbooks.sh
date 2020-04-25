#!/bin/bash

# echo "Installing any ansible requirements"
# cd ansible
# pip install -r ansible_requirements.txt

# echo "Installing sshpass which let's us use a password to SSH instead of .pem"
# sudo apt-get install sshpass

# echo "Source .env for some required env vars to run playbooks"
# source .env

# echo "Check for required values"
# if [[ -z $ANSIBLE_VAULT_PASSWORD ]]; then
#     echo "ANSIBLE_VAULT_PASSWORD environment variable required to run"
#     exit 1
# fi
# if [[ -z $ANSIBLE_SSH_PASSWORD ]]; then
#     echo "ANSIBLE_SSH_PASSWORD environment variable required to run"
#     exit 1
# fi

# echo "Run the playbooks..."
# echo "$ANSIBLE_VAULT_PASSWORD" >> password
# export ANSIBLE_VAULT_PASSWORD_FILE=password
# ansible-playbook -i inventories site.yml
# unset ANSIBLE_VAULT_PASSWORD_FILE
# rm -rf password

# cd -

  # Run Ansible for QA deployment on ec2
  # - cd ansible/ && make run-docker-qa-playbook
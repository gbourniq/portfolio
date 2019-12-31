#!/bin/bash

set -xe #  exit as soon as any command returns a nonzero status

# Populate ansible vault passphrase
touch ec2-deployment/roles/setup/vars/ansible-vault-pw
if [ -z "${ANSIBLE_VAULT_PASSPHRASE}" ]; then
    echo "Environment variable ANSIBLE_VAULT_PASSPHRASE is empty. Need to run source .env"
else
    echo ${ANSIBLE_VAULT_PASSPHRASE} > ec2-deployment/roles/setup/vars/ansible-vault-pw
fi

# Checking ansible command syntax...
make ansible-checksyntax

# Populate inventory file with ec2 public IP address. commented to avoid fail in travis CI
# make ansible-define-host

# Running ansible playbook for machine setup
make ansible-instance-setup
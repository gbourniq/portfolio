# Set shell
SHELL=/bin/bash -e -o pipefail

before-playbook: env-validation
	@ echo "${ANSIBLE_VAULT_PASSWORD}" > /tmp/ansible-vault-pw

after-playbook:
	@ rm -rf /tmp/ansible-vault-pw

docker-deploy-playbook:
	@ ansible-playbook \
		-i inventories \
		--vault-id /tmp/ansible-vault-pw \
		docker_deployment.yml \
		--skip-tags="slack-notification-qa,compose-down,stop-instance" \
		-vv

docker-qa-playbook:
	@ ansible-playbook \
		-i inventories \
		--vault-id /tmp/ansible-vault-pw \
		docker_deployment.yml \
		--skip-tags="slack-notification-dev" \
		-vv

.PHONY: run-docker-deploy-playbook run-docker-qa-playbook
run-docker-deploy-playbook: before-playbook docker-deploy-playbook after-playbook
run-docker-qa-playbook: before-playbook docker-qa-playbook after-playbook

###### UTILS ######

# Ensure all environment variables are set
.PHONY: env-validation
env-validation:
	@ INFO "Checking if required environment variables are set..."
	@ ../scripts/env_validation.sh
	@ SUCCESS "All good!"

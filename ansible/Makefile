# Set shell
SHELL=/bin/bash -e -o pipefail

# Cosmetics
RED := "\e[1;31m"
YELLOW := "\e[1;33m"
GREEN := "\033[32m"
NC := "\e[0m"
INFO := @bash -c 'printf ${YELLOW}; echo "[INFO] $$1"; printf ${NC}' MESSAGE
MESSAGE := @bash -c 'printf ${NC}; echo "$$1"; printf ${NC}' MESSAGE
SUCCESS := @bash -c 'printf ${GREEN}; echo "[SUCCESS] $$1"; printf ${NC}' MESSAGE
WARNING := @bash -c 'printf ${RED}; echo "[WARNING] $$1"; printf ${NC}' MESSAGE


###### ANSIBLE ######

.PHONY: run-docker-deploy-playbook run-docker-qa-playbook

before-playbook: env-vars-check
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
		docker_qa_deployment.yml \
		--skip-tags="slack-notification-dev" \
		-vv

postgres-backup-playbook:
	@ ansible-playbook \
		-i inventories \
		--vault-id /tmp/ansible-vault-pw \
		postgres_backup.yml \
		-vv

run-docker-deploy-playbook: before-playbook docker-deploy-playbook after-playbook
run-docker-qa-playbook: before-playbook docker-qa-playbook after-playbook
run-postgres-backup-playbook: before-playbook postgres-backup-playbook after-playbook

###### UTILS ######

# Ensure all environment variables are set
.PHONY: env-vars-check
env-vars-check:
	${INFO} "Checking if required environment variables are set..."
	@ ../scripts/env_vars_check.sh
	${SUCCESS} "All good!"

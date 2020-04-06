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

.PHONY: docker-deployment-playbook

before-playbook: env-vars-check
	@ echo "${ANSIBLE_VAULT_PASSWORD}" > /tmp/ansible-vault-pw

after-playbook:
	@ rm -rf /tmp/ansible-vault-pw

docker-playbook:
	@ cd ansible/ && ansible-playbook \
					-i inventories \
					--vault-id /tmp/ansible-vault-pw \
					docker_deployment.yml -vv

docker-deployment-playbook: before-playbook docker-playbook after-playbook



###### UTILS ######

# Ensure all environment variables are set
.PHONY: env-vars-check
env-vars-check:
	${INFO} "Checking if required environment variables are set..."
	@ ./utils/env_vars_check.sh
	${SUCCESS} "All good!"

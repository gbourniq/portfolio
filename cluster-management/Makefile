# Set shell
SHELL=/bin/bash -e -o pipefail

# Cosmetics
RED := "\e[1;31m"
YELLOW := "\e[1;33m"
GREEN := "\033[32m"
NC := "\e[0m"
INFO := @bash -c 'printf $(YELLOW); echo "ANSIBLE => $$1"; printf $(NC)' MESSAGE
INSTRUCTION := @bash -c 'printf $(NC); echo "   $$1"; printf $(NC)' MESSAGE
SUCCESS := @bash -c 'printf $(GREEN); echo "[SUCCESS] $$1"; printf $(NC)' MESSAGE
WARNING := @bash -c 'printf $(RED); echo "[WARNING] $$1"; printf $(NC)' MESSAGE


#################################################################
########### DOCKER-SWARM - SINGLE INSTANCE MANAGEMENT ###########
#################################################################

# Common settings
DOCKER_SWARM_DIR=docker-swarm
INSTANCE_IP_SWARM=52.47.178.237

########### RUN-INSTANCE PLAYBOOK ###########

swarm-instance-stop:
	${INFO} "Stopping instances with the following tag: type=swarm"
	@ ansible-playbook ${DOCKER_SWARM_DIR}/run-instance-playbook.yml \
		-i ${DOCKER_SWARM_DIR}/inventory.yml \
		--tags=stop-instance \
		-vv
	${SUCCESS} "Instance stopped successfully"

swarm-instance-start:
	${INFO} "Starting instances with the following tag: type=swarm"
	@ ansible-playbook ${DOCKER_SWARM_DIR}/run-instance-playbook.yml \
		-i ${DOCKER_SWARM_DIR}/inventory.yml \
		--tags=start-instance \
		-vv
	${SUCCESS} "Instance starting at ${INSTANCE_IP_SWARM}"
	

########### DEPLOYMENT PLAYBOOK ###########

swarm-deployment-all: swarm-instance-start swarm-setup-instance swarm-docker-prune swarm-clone-repo swarm-deploy-stack

swarm-setup-instance:
	${INFO} "Install dependencies: Git, Python, Docker ..."
	@ ansible-playbook ${DOCKER_SWARM_DIR}/deployment-playbook.yml \
		-i ${DOCKER_SWARM_DIR}/inventory.yml \
		-vv \
		--tags=setup-instance
	${SUCCESS} "Instance setup complete"

swarm-docker-prune:
	${INFO} "Remove any existing docker components: stacks, containers, images, volumes and networks..."
	@ ansible-playbook ${DOCKER_SWARM_DIR}/deployment-playbook.yml \
		-i ${DOCKER_SWARM_DIR}/inventory.yml \
		-vv \
		--tags=docker-prune
	${SUCCESS} "Cleanup complete"

swarm-clone-repo:
	${INFO} "Clean up existing local files and clone github repo..."
	@ ansible-playbook ${DOCKER_SWARM_DIR}/deployment-playbook.yml \
		-i ${DOCKER_SWARM_DIR}/inventory.yml \
		--vault-id ~/.ssh/ansible-vault-pw \
		-vv \
		--tags=clone-repo
	${SUCCESS} "Cloning complete"

swarm-deploy-stack:
	${INFO} "Running ansible playbook to start services"
	@ ansible-playbook ${DOCKER_SWARM_DIR}/deployment-playbook.yml \
		-i ${DOCKER_SWARM_DIR}/inventory.yml \
		--vault-id ~/.ssh/ansible-vault-pw \
		-vv \
		--tags=deploy-stack
	${SUCCESS} "Start services complete"


#######################################################
########### KUBERNETES - CLUSTER MANAGEMENT ###########
#######################################################

# k8s-checksyntax:
# 	${INFO} "Checking ansible command syntax..."
# 	@ ansible-playbook -i ec2-deployment/inventory.yml ec2-deployment/site.yml --syntax-check
# 	${SUCCESS} "Syntax check complete..."

# cluster-configure:
# 	${INFO} "Cluster configuration instructions"
# 	${INSTRUCTION} "1. Run <make cluster-create> command"
# 	${INSTRUCTION} "2. SSH into Master:"
# 	${INSTRUCTION} "   Set hostname with <sudo hostnamectl set-hostname k8s-master>"
# 	${INSTRUCTION} "   Run master_firstrun.sh script"
# 	${INSTRUCTION} "   Copy the <kubeadm join ...> command from the output"
# 	${INSTRUCTION} "3. SSH into each Nodes:"
# 	${INSTRUCTION} "   Set hostname with <sudo hostnamectl set-hostname k8s-node-X>"
# 	${INSTRUCTION} "   Run node_firstrun.sh script"
# 	${INSTRUCTION} "   Run the <sudo kubeadm join ...> command"
	

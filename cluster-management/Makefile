DEPLOY_DIR=docker-deployment
ANSIBLE_DIR=ec2-deployment
SHELL := /bin/bash


# Include env variables
include .ansible-env
include ec2-deployment/.current-instance-id-env
# Common settings
include Makefile.settings

# Set shell
SHELL=/bin/bash -e -o pipefail

# Common settings
ANSIBLE_DIR=cluster-deployment
MASTER_INSTANCE_IP=ec2-15-188-177-177.eu-west-3.compute.amazonaws.com

# Cosmetics
RED := "\e[1;31m"
YELLOW := "\e[1;33m"
GREEN := "\033[32m"
NC := "\e[0m"
INFO := @bash -c 'printf $(YELLOW); echo "=> $$1"; printf $(NC)' MESSAGE
INSTRUCTION := @bash -c 'printf $(NC); echo "   $$1"; printf $(NC)' MESSAGE
SUCCESS := @bash -c 'printf $(GREEN); echo "[SUCCESS] $$1"; printf $(NC)' MESSAGE
WARNING := @bash -c 'printf $(RED); echo "[WARNING] $$1"; printf $(NC)' MESSAGE


# Common settings
include Makefile.settings

packer-build-ami:
	${INFO} "Running packer.json to build an Amazon Machine Image..."
	@ packer build ${PACKER_DIR}/packer.json

ansible-checksyntax:
	${INFO} "Checking ansible command syntax..."
	@ ansible-playbook -i ${ANSIBLE_DIR}/inventory.yml ${ANSIBLE_DIR}/cluster_lifecycle_playbook.yml --syntax-check
	${SUCCESS} "Syntax check complete"

cluster-create:
	${INFO} "Running ansible playbook to create the following ec2 instances: 1 Master, X Nodes"
	@ ansible-playbook ${ANSIBLE_DIR}/cluster_lifecycle_playbook.yml \
		--vault-id user@~/.ssh/ansible-vault-pw \
		--tags=cluster-create \
		-vvv
	${SUCCESS} "Instances created successfully with tag: type=k8s-cluster"


cluster-configure:
	${INFO} "Cluster configuration instructions"
	${INSTRUCTION} "1. Run <make cluster-create> command"
	${INSTRUCTION} "2. SSH into Master:"
	${INSTRUCTION} "   Set hostname with <sudo hostnamectl set-hostname k8s-master>"
	${INSTRUCTION} "   Run master_firstrun.sh script"
	${INSTRUCTION} "   Copy the <kubeadm join ...> command from the output"
	${INSTRUCTION} "3. SSH into each Nodes:"
	${INSTRUCTION} "   Set hostname with <sudo hostnamectl set-hostname k8s-node-X>"
	${INSTRUCTION} "   Run node_firstrun.sh script"
	${INSTRUCTION} "   Run the <sudo kubeadm join ...> command"
	

cluster-stop:
	${INFO} "Stopping all instances with the following tag: type=k8s-cluster"
	@ ansible-playbook ${ANSIBLE_DIR}/cluster_lifecycle_playbook.yml \
		--vault-id user@~/.ssh/ansible-vault-pw \
		--tags=cluster-stop \
		-vv
	${SUCCESS} "Cluster stopped successfully"

cluster-start:
	${INFO} "Starting all instances with the following tag: type=k8s-cluster"
	@ ansible-playbook ${ANSIBLE_DIR}/cluster_lifecycle_playbook.yml \
		--vault-id user@~/.ssh/ansible-vault-pw \
		--tags=cluster-start \
		-vv
	${SUCCESS} "Cluster starting... Master running on ${MASTER_INSTANCE_IP}"
	
# Executes a full workflow
ansible-all: ansible-checksyntax ansible-instance-setup ansible-deploy-build ansible-instance-cleanup ansible-deploy-prod

ansible-checksyntax:
	${INFO} "Checking ansible command syntax..."
	@ ansible-playbook -i ec2-deployment/inventory.yml ec2-deployment/site.yml --syntax-check
	${SUCCESS} "Syntax check complete..."

instance-setup:
	${INFO} "Running ansible playbook for machine setup"
	@ ansible-playbook -i ec2-deployment/inventory.yml --vault-id ec2-deployment/roles/setup/vars/ansible-vault-pw ec2-deployment/site.yml -vv --tags=system,instance-setup
	${SUCCESS} "Instance setup complete"

instance-cleanup:
	${INFO} "Remove running containers and all images"
	@ ansible-playbook -i ec2-deployment/inventory.yml --vault-id ec2-deployment/roles/setup/vars/ansible-vault-pw ec2-deployment/site.yml -vv --tags=docker-cleanup
	${SUCCESS} "Cleanup complete"

# create github pwd variable in ansible vault?
# remove ansible vault text file
clone-repo: ansible-instance-cleanup
	${INFO} "Running ansible playbook to clone github repo"
	@ ansible-playbook -i ec2-deployment/inventory.yml --vault-id ec2-deployment/roles/setup/vars/ansible-vault-pw ec2-deployment/site.yml -vv --tags=clone-repo
	${SUCCESS} "Cloning complete"

docker-build-workflow:
	${INFO} "Running ansible playbook to build images"
	@ ansible-playbook -i ec2-deployment/inventory.yml --vault-id ec2-deployment/roles/setup/vars/ansible-vault-pw ec2-deployment/site.yml -vv --tags=build-images
	${SUCCESS} "Build images complete"

# create docker login 

docker-deploy-stack:
	${INFO} "Running ansible playbook to start services"
	@ ansible-playbook -i ec2-deployment/inventory.yml --vault-id ec2-deployment/roles/setup/vars/ansible-vault-pw ec2-deployment/site.yml -vv --tags=start-services
	${SUCCESS} "Start services complete"
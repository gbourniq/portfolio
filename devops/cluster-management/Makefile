ANSIBLE_DIR=cluster-deployment
PACKER_DIR=create-AMIs
MASTER_INSTANCE_IP=ec2-15-188-177-177.eu-west-3.compute.amazonaws.com

SHELL := /bin/bash

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
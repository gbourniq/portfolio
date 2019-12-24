ANSIBLE_DIR=cluster-deployment
MASTER_INSTANCE_IP=ec2-15-188-177-177.eu-west-3.compute.amazonaws.com

SHELL := /bin/bash

# Common settings
include Makefile.settings

# ansible-checksyntax:
# 	${INFO} "Checking ansible command syntax..."
# 	@ ansible-playbook -i ${ANSIBLE_DIR}/inventory.yml ${ANSIBLE_DIR}/cluster_lifecycle_playbook.yml --syntax-check
# 	${SUCCESS} "Syntax check complete"

run:
	${INFO} "Running python manage.py runserver"
	@ python manage.py runserver
	${SUCCESS} "Server started successfully"


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
	

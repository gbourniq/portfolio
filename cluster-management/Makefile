DEPLOY_DIR=docker-deployment
ANSIBLE_DIR=ec2-deployment
SHELL := /bin/bash


# Include env variables
include .ansible-env
include ec2-deployment/.current-instance-id-env
# Common settings
include Makefile.settings


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
	
clone-repo: ansible-instance-cleanup
	${INFO} "Running ansible playbook to clone github repo"
	@ ansible-playbook -i ec2-deployment/inventory.yml --vault-id ec2-deployment/roles/setup/vars/ansible-vault-pw ec2-deployment/site.yml -vv --tags=clone-repo
	${SUCCESS} "Cloning complete"

docker-build-workflow:
	${INFO} "Running ansible playbook to build images"
	@ ansible-playbook -i ec2-deployment/inventory.yml --vault-id ec2-deployment/roles/setup/vars/ansible-vault-pw ec2-deployment/site.yml -vv --tags=build-images
	${SUCCESS} "Build images complete"

docker-deploy-stack:
	${INFO} "Running ansible playbook to start services"
	@ ansible-playbook -i ec2-deployment/inventory.yml --vault-id ec2-deployment/roles/setup/vars/ansible-vault-pw ec2-deployment/site.yml -vv --tags=start-services
	${SUCCESS} "Start services complete"
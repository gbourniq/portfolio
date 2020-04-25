#!/bin/bash

# echo "Setting PYTHONPATH to $PWD for tarball script imports to work properly"
# export PYTHONPATH=$PWD

# echo "Installing any needed dependencies for docker compose tarball creation"
# pip install -r docker_deployment/deployment_requirements.txt

# python docker_deployment/build_docker_deploy_tarball.py -dp # fill in dummy vals b/c this is for QA auto deploys

# echo "creating directory docker_compose_artifacts and moving docker compose files there"
# mkdir -p docker_compose_artifacts
# mv docker_deployment/bin/mvp_docker_deploy.tar.gz docker_compose_artifacts/mvp_docker_deploy.tar.gz


  - make upload-docker-deploy-tarball
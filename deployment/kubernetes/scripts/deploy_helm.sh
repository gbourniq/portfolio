#!/usr/bin/env bash

# exit with error status on first failure
set -e

# Set directory paths
SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )
PARENT_DIR=$(dirname "$SCRIPT_DIR")
CHART_DIR="${PARENT_DIR}/portfolio-app"

# Set release name for deployments
RELEASE_NAME="dev"

# Set helm repositories
HELM_BITNAMI_REPO_NAME="${HELM_BITNAMI_REPO_NAME:-bitnami}"
HELM_BITNAMI_REPO_URL="${HELM_BITNAMI_REPO_URL:-https://charts.bitnami.com/bitnami}"
trap "echo 'Something went wrong! Exiting...' && exit 1" ERR SIGHUP SIGINT SIGQUIT SIGTERM


function deploy_chart() {
  update_chart_dependencies
  INFO "Install ${RELEASE_NAME} release for $CHART_DIR chart..."
  helm upgrade ${RELEASE_NAME} "${CHART_DIR}" --install --wait
}


INFO "Begin deployment..."

# Source the following functions:
# - are_commands_available
# - update_chart_dependencies
source "${SCRIPT_DIR}"/utils.sh

# Login to docker
echo "${DOCKER_PASSWORD}" | docker login --username "${DOCKER_USER}" --password-stdin

# Check if all required commands are available locally
are_commands_available

# Deploy chart
deploy_chart

SUCCESS "Successfully deployed portfolio-app chart with Helm!"
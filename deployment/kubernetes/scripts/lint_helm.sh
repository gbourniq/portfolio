#!/usr/bin/env bash

# exit with error status on first failure
set -e

# Set directory paths
SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )
PARENT_DIR=$(dirname "$SCRIPT_DIR")
CHART_DIR="${PARENT_DIR}/portfolio-app"
INFO "$CHART_DIR"

# Set releaçse name for deployments
RELEASE_NAME="dev"

# Set helm repositories
HELM_BITNAMI_REPO_NAME="${HELM_BITNAMI_REPO_NAME:-bitnami}"
HELM_BITNAMI_REPO_URL="${HELM_BITNAMI_REPO_URL:-https://charts.bitnami.com/bitnami}"

trap "echo 'Something went wrong! Exiting...' && exit 1" ERR SIGHUP SIGINT SIGQUIT SIGTERM


function run_lint() {
  update_chart_dependencies
  INFO "Linting $CHART_DIR chart..."
  helm lint "${CHART_DIR}"
}


INFO "Begin linting..."

# Source the following functions:
# - update_chart_dependencies
# - are_commands_available
source "${SCRIPT_DIR}"/utils.sh

# Login to docker
echo "${DOCKER_PASSWORD}" | docker login --username "${DOCKER_USER}" --password-stdin

# Check if all required commands are available locally
are_commands_available

# Lint chart
run_lint

SUCCESS "Helm lint successful!"
#!/usr/bin/env bash

# exit with error status on first failure
set -e

# Set directory paths
SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )
PARENT_DIR=$(dirname "$SCRIPT_DIR")
CHART_DIR="${PARENT_DIR}/portfolio-app"
OUTPUT_DIR="${PARENT_DIR}/bin"

# Set release name for deployments
RELEASE_NAME="dev"

# Set helm repositories
HELM_BITNAMI_REPO_NAME="${HELM_BITNAMI_REPO_NAME:-bitnami}"
HELM_BITNAMI_REPO_URL="${HELM_BITNAMI_REPO_URL:-https://charts.bitnami.com/bitnami}"

trap "echo 'Something went wrong! Exiting...' && exit 1" ERR SIGHUP SIGINT SIGQUIT SIGTERM


function deploy_chart() {
  update_chart_dependencies

  # Create a temporary output directory for helm to write the files to
  mkdir -p "${OUTPUT_DIR}"

  INFO "Generate K8s chart templates for $CHART_DIR..."
  helm template ${RELEASE_NAME} "${CHART_DIR}" --output-dir "${OUTPUT_DIR}" --dry-run
  # Package the files from the temp output dir (tar)
  CHART_VERSION=$(helm show chart "${CHART_DIR}" | grep '^version: ' | awk -F ' ' '{print $2}')
  tar -czvf "${PARENT_DIR}/portfolio_kubernetes_${CHART_VERSION}.tar.gz" -C "${OUTPUT_DIR}" .
}

INFO "Begin generation of k8s files from Helm template..."

# Source the following functions:
# - update_chart_dependencies
# - are_commands_available
source "${SCRIPT_DIR}"/utils.sh

# Login to docker
echo "${DOCKER_PASSWORD}" | docker login --username "${DOCKER_USER}" --password-stdin

# Check if all required commands are available locally
are_commands_available

# Deploy chart
deploy_chart

SUCCESS "Successfully generated k8s files from Helm templates!"
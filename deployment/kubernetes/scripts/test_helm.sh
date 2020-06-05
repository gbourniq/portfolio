#!/usr/bin/env bash

# exit with error status on first failure
set -e

# Set directory paths
SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )
PARENT_DIR=$(dirname "$SCRIPT_DIR")
CHART_DIR="${PARENT_DIR}/portfolio-app"
RELEASE_NAME="dev"

HELM_BITNAMI_REPO_NAME="${HELM_BITNAMI_REPO_NAME:-bitnami}"
HELM_BITNAMI_REPO_URL="${HELM_BITNAMI_REPO_URL:-https://charts.bitnami.com/bitnami}"

RELEASE_NAME="test"
RELEASE_LABEL="app.kubernetes.io/instance=${RELEASE_NAME}"

trap "echo 'Something went wrong! Exiting...' && exit 1" ERR SIGHUP SIGINT SIGQUIT SIGTERM


function clean_up_test_pods() {
  # The test pods should be deleted immediately by the helm hooks, but if for some reasons
  # this didn't happen, then we need to remove them manually.
  running_pods=$(kubectl get po -o name)
  if [[ $(echo "${running_pods}" | grep -c test-connection) -gt 0 ]]; then
    running_test_pods=$(echo "${running_pods}" | grep test-connection)
    kubectl delete "${running_test_pods}"
  fi
}

function run_test() {
  update_chart_dependencies

  # If the chart is already installed for this release, then uninstall it
  if [[ $(helm list | grep -c ${RELEASE_NAME} | cat ) -gt 0 ]]; then
      echo "Uninstalling ${RELEASE_NAME} release..."
      helm uninstall ${RELEASE_NAME}
      until [[ $(kubectl get po -l "${RELEASE_LABEL}" | wc -l) -eq 0 ]]; do
        printf "\r Waiting for all pods to be fully terminated...\n"
        sleep 10
      done
  fi

  INFO "Installing and testing ${RELEASE_NAME} release..."
  # helm install ${RELEASE_NAME} "${CHART_DIR}" --wait --timeout=15m --debug -v=4
  helm install ${RELEASE_NAME} "${CHART_DIR}" --wait --timeout=15m

  are_all_deployments_ready
  helm test ${RELEASE_NAME}
  helm uninstall ${RELEASE_NAME}
}

INFO "Begin testing..."

# Source the following functions:
# - update_chart_dependencies
# - are_commands_available
# - are_all_deployments_ready
source "${SCRIPT_DIR}"/utils.sh

# Login to docker
echo "${DOCKER_PASSWORD}" | docker login --username "${DOCKER_USER}" --password-stdin

# Check if all required commands are available locally
are_commands_available

# Run helm test and clean up
run_test
clean_up_test_pods

SUCCESS "Helm tests successful!"
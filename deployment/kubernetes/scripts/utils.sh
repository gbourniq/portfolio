#!/usr/bin/env bash

# exit with error status on first failure
set -e

function remove_chart_dependencies()
{
  MESSAGE "Removing dependencies for chart ${CHART_DIR}"
  rm -rf "${CHART_DIR}"/charts "${CHART_DIR}"/Chart.lock
}

function are_commands_available() {
  REQUIRED_COMMANDS=(helm kubectl)
  MESSAGE "Checking if all commands are available (${REQUIRED_COMMANDS[*]})"
  for command in "${REQUIRED_COMMANDS[@]}"; do
    if [[ -z $(command -v "$command") ]]; then
      MESSAGE "$command is not installed! Aborting."
      exit 1
    fi
  done
}

function update_chart_dependencies() {
  MESSAGE "Add community Bitnami Helm Chart repo and get updates from repo"
  helm repo add "${HELM_BITNAMI_REPO_NAME}" "${HELM_BITNAMI_REPO_URL}"
  helm repo update
  
  MESSAGE "Updating chart dependencies..."
  remove_chart_dependencies
  helm dependency update "${CHART_DIR}"
}

function get_deployments() {
# Get status of the deployments
  deployments_status=$(kubectl get deployments -l "${RELEASE_LABEL}" -o=jsonpath='{range .items[*]}{.status.conditions[?(@.type=="Available")].status}{"\n"}{end}')
  echo "$deployments_status"
}

function are_all_deployments_ready() {
# Check if deployments are ready
  until [[ get_deployments \
            && ($(get_deployments | wc -l) -eq $(get_deployments | grep True | wc -l)) ]]; do
    printf "\r Waiting for all deployments to be ready...\n"
    sleep 10
  done
}





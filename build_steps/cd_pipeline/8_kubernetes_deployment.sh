#!/bin/bash

# Exit on error
set -e

deployment/kubernetes/scripts/lint_helm.sh
deployment/kubernetes/scripts/test_helm.sh
deployment/kubernetes/scripts/generate_helm_templates.sh
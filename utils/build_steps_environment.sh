echo "Check for required values"

if [[ -z $DOCKER_USER ]]; then
    echo "DOCKER_USER environment variable required to run"
    exit 1
fi
if [[ -z $DOCKER_PASSWORD ]]; then
    echo "DOCKER_PASSWORD environment variable required to run"
    exit 1
fi
if [[ -z $ANSIBLE_HOST ]]; then
    echo "ANSIBLE_HOST environment variable required to run"
    exit 1
fi
if [[ -z $ANSIBLE_VAULT_PASSWORD ]]; then
    echo "ANSIBLE_VAULT_PASSWORD environment variable required to run"
    exit 1
fi
if [[ -z $ANSIBLE_SSH_PASSWORD ]]; then
    echo "ANSIBLE_SSH_PASSWORD environment variable required to run"
    exit 1
fi
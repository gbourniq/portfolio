# Ansible MVP + Phoenix

#### A playbook for spinning up specified versions of Phoenix and MVP and triggering dags.

------------------------------------------

## 1. Usage

### - Running the playbooks
- First see .env for setting any necessary env vars
- `ansible-playbook -i inventories site.yml` Runs the every playbook for all URLS.

## 2. Project setup

### `ansible/site.yml`
This is the entrypoint to the master usage of ansible for our use cases.
It imports all of the playbooks. 

### `ansible/roles/`
Roles are ways of automatically loading certain vars_files, tasks, and handlers based on a known file structure. Grouping content by roles also allows easy sharing of roles with other users.

### `ansible/inventories`
Inventories in ansible are a pattern for grouping managed nodes/hosts.


### Playbooks
- `ansible/fresh_bare_metal_deployment.yml` 
deploys the latest bare metal deployment of (not an upgrade) and starts phoenix with docker

- `ansible/fresh_docker_deployment.yml` 
deploys the latest docker-compose (not an upgrade) and starts phoenix with docker

### Encryption of credentials
The file `roles/docker_login/vars/main.yml` is encrpyted by ansible-vault.
This yml contains the `docker_username` and `docker_password`.  The user is the user
we typically use for client deployments.
The `ANSIBLE_VAULT_PASSWORD_FILE` environment variable should point to a plain test file containing the password (outside of source control).

### Testing
In the future we will use molecule for testing.


TEMPORARY: git clone repo > means always running Master version...
which is good for QA, but not for actual deployments.
Options:
- package it into release with packaged image and/or portfolio.tar.gz
- git checkout <branch>
# Ansible documentation

#### Ansible playbooks to test application deployments on fresh EC2 instances 

------------------------------------------

## Pre-requisites

### Create an AMI

The Ansible playbooks are expected to launch instances based on an AMI with the following software and packages installed:
- AWS CLI package
- Python / Pip
- Docker and Docker-Compose
- Logged in to Dockerhub

To create the AMI, please follow the steps below.

1. Launch a new Amazon Linux 2 instance

2. Run the following commands
```
sudo yum update -y

sudo yum install awscli python3 python3-pip make curl -y
sudo alias python='python3'
sudo pip3 install docker docker-compose boto3 botocore

sudo amazon-linux-extras install docker -y
sudo service docker start
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user
sudo docker info

sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose version

sudo docker login --username=<username>
```


3. Create an AMI out of the instance


## Usage

### Running the playbooks

The following command run the docker_deployment playbook:
```bash
ansible-playbook \
    -i inventories \
    --vault-id user@~/.ssh/ansible-vault-pw \
    docker_deployment.yml \
    -vv
```
Alternatively, a make command can be used from the project root directory:
```bash
cd portfolio/  # if not already at the root of the repository.
make run-ansible-playbook
```

### Encryption of credentials

The `ansible-vault-pw` file mentioned in the command above, contains the `ansible vault passphrase`, which is essentially a string used by Ansible to encrypt and decrypt sensitive variables.

To encrypt a variable, run a command such as:
```bash
ansible-vault encrypt_string --vault-id user@~/.ssh/ansible-vault-pw <sensitive-value> --name <var-name>
```
This will output the encrypted variable, which can be inserted in a `<role-name>/vars/main.yaml` to be used within a role.
```
var-name: !vault |
    $ANSIBLE_VAULT;1.2;AES256;user
    30636330353937373466313931316664356235323061393531353564303535346366343162646635
    3038336463663531663335376635303336343262666339340a613233643934663164366337613666
    39333839323430336532316138393437356239356465316565326232666633626465383864366337
    3532326531303630630a626563613433373138363337353166303666663165626535663639373334
    39313431633663323338626436336261323439303461616239323465336134363734
```


## Set Environment Variables for Ansible

|**Name**                      |**Description**                                                               |
|------------------------------|------------------------------------------------------------------------------|
|`RUN_ANSIBLE_PLAYBOOK`        | Must be set to `True` to run the Ansible playbook within the CD pipeline     |
|`ANSIBLE_VAULT_PASSWORD`      | Passphrase used to encrypt/decrypt secret variables (see /ansible/README.md) |
|`ANSIBLE_INSTANCE_ID`         | To start and stop AWS EC2 instance                                           |
|`ANSIBLE_HOST_IP`             | Used in Ansible `inventories` to specify ansible_host                        |
|`ANSIBLE_HOST_NAME`           | Used by docker-compose up role to check if app returns 200                   |
|`ANSIBLE_HOST_PUBLIC_DNS`     | To start and stop AWS EC2 instance                                           |
|`PORTFOLIO_ROOT_DIR`          | For ansible roles to navigate on the remote and run commands                 | 
|`SSL_*_S3_OBJECT_PATH`        | S3 paths for SSL private key and certificate (required for nginx)            |
|`SSL_*_HOST_PATH`             | EC2 host path where SSL private key and certificate are located              |
|`ENABLE_SLACK_NOTIFICATION`   | Can be set to `False` to skip slack notification when app is up              |
|`QA_INSTANCE_TIME_MINUTES`    | Number of minutes the app should be running before the instance is shut down | 
|`SLACK_TOKEN`                 | Token for Ansible to connect to the slack app                                |



## Project setup

### Ansible inventories

Inventories in ansible are a pattern for grouping managed nodes/hosts. They are located in `ansible/inventories/`.


### Ansible playbooks

Playbooks contain the steps which are set to execute on a particular machine.

This repository contains the following playbooks:

- `docker_deployment.yml`: set up an EC2 instance and deploy portfolio application (`prod` build) using the latest *docker deploy tarball* created from the CD pipeline (step `7_build_and_push_docker_compose_tarball.sh`).

- `kubernetes_deployment.yml`: similar to the above using Helm and Kubernetes (WIP)

- `stop_instance.yml`: stop the EC2 instance whether the above playbooks are successful or not.

### Ansible roles

Roles can be found in `ansible/roles/` and are ways of automatically loading certain vars_files, tasks, and handlers based on a known file structure. Grouping content by roles also allows easy sharing of roles with other users.

For example, the `docker_deployment.yml` playbook runs the following roles:

- `start_instance`: start an ec2 instance with a given instance-id, and wait for instance to be running

- `setup_instance`: install required packages (pip, awscli, make, ...), and install Docker / docker-compose

- `prepare_deployment`: docker prune all, delete existing project root directory, download the latest docker deployment folder from S3 (built by the CD pipeline), download SSL files for nginx from S3

- `docker_compose_up`: start docker services, wait until services are healthy, and app is running

- `test_postgres_backup`: run postgres back up scripts (dump to S3, and restore from S3)

- `send_slack_notification`: send slack message to notify user the app is up, 

- `pause_playbook`: pause playbook for `<QA_INSTANCE_TIME_MINUTES>` minutes, to give enough time for a user to navigate around the UI and test app functionalities

- `docker_compose_down`: stop and remove docker services


### Testing

> TIP: molecule can be used for testing.
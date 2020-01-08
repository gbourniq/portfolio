# Portfolio Application
This project is a Django web application that can be used by anyone as a template to create a blog or any personal portfolio. 

By accessing the Django Admin section, it is possible to easily manage the following website content:
The following component can be created
- Categories
- Sub-categories
- Articles 

To do:
* Diagram showing relationship between Categories, Sub-Categories and Articles
* Screenshot of main application page


## Contents

- [Application Architecture](#application-architecture)
- [Quick Start](#quick-start)
- [Manual Deployment Options](#manual-deployment-options)
- [Automated Deployment Options](#automated-deployment-options)
- [Backing up Postgres](#backing-up-postgres)


## Application Architecture
The application is composed of the following micro-services:
- Nginx as a reverse proxy
- Django web server
- Celery for asynchronous tasks
- Redis as a message broker and caching
- Postgres to store web server data
- (MongoDB to store image data?)

In order to faciliate testing and deployment tasks, a full CI/CD workflow has been implemented using Travis CLI, Ansible, and Docker/Kubernetes.


## Quick Start

### Prerequisites
Before building and running the application locally, your system must meet the following prerequisites :

1. Install dependencies
```
$ conda env create -f environment.yml
$ conda env activate portfolio-env
```

2. Set the following environment variables
|**Environment Variables**     |**What it does**                                                  |
|------------------------------|------------------------------------------------------------------|
|`DEBUG`                       | Django variable in settings.py                                   |
|`SECRET_KEY`                  | Django variable in settings.py                                   |
|`EMAIL_HOST_USER`             | Email addr. for users to send messages (contact page) (optional) |
|`EMAIL_HOST_PASSWORD`         | Email address password (optional)                                |

3. Create a local Postgres database `myportfoliodb`

### Running the app locally (dev/test)
Running the server locally without external docker services
```
$ cd app/
$ source .env
$ make create-superuser
$ make tests-run
$ make tests-coverage
$ make run
$ make logs-show
```

Note: The following services will not run (require docker containers)
- Celery
- Redis
- Nginx 


## Manual Deployment Options

### Local deployment with docker-compose (dev/test)
```
$ cd deployment/
$ make rebuild-app-image
$ make deploy-compose
$ make services-health
$ make login && make publish-app-image
$ make clean-environment
```

Note: Travis CLI (.travis.yml) workflow performs automatically the steps describe above.
For every push to master, the Docker-based continuous delivery workflow looks like this:
- Test app source code
- Package app source code into a docker container
- Create all services with docker-compose (Nginx, Django server, Celery, Redis, and Postgres)
- Check that all services are up and healthy

### Publishing release image
The final stage is to publish the release images for the django app. This assumes that all services are up locally and healthy and a satisfactory image `portfolio_app` has been created from the previous step.
```
$ make publish-app-image
```

Note: To be able to publish your release images, you will need to specify a Docker registry that you have write access to.
This can be achieved by editing the `PROJECT VARIABLES` in [`Makefile.settings`](./deployment/Makefile.settings) and configuring the `DOCKER_USER` and `DOCKER_REGISTRY` settings.

### Ubuntu Deployment with docker-compose (dev/test)
```
$ cd deployment/
$ docker-compose -f docker-deployment/docker-compose.yml up
$ make watch-containers (separate terminal)
```

### Ubuntu Deployment with Docker Swarm (prod)
```
$ cd deployment/
$ make stack-deploy
$ make watch-containers (separatez terminal)
```

### Ubuntu Deployment with Kubernetes (prod)
```
Work in progress
```

## Automated Deployment Options

### Automated Deployment on Ubuntu with Docker Swarm and Ansible
Ensure the Manager node instance is running:
```
$ cd cluster-management
$ make swarm-instance-start
```

### Deployment without instance setup (docker and other dependencies installation)
```
$ make swarm-deployment-no-setup
```
At a high level this command triggers an Ansible script to perform the following tasks:
- Clone repo
- Prune all docker components
- Run stack deployment
- Check services are up and healthy

### Deployment without instance setup (docker and other dependencies installation)
```
$ make swarm-deployment-all
```
At a high level this command triggers an Ansible script to perform the following tasks:
- Install dependencies (eg. Docker, Docker-Compose, etc)
- Clone repo
- Prune all docker components
- Run stack deployment
- Check services are up and healthy

## Backing up Postgres
This assume the postgres container is up and running on the docker swarm manager instance.
```
make swarm-backup-postgres
```
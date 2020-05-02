[![Travis Build Status](https://travis-ci.com/gbourniq/portfolio.svg?branch=master)](https://travis-ci.com/gbourniq/portfolio)

# Portfolio Application
This is a personal project is a 
Django web application that can be used as a template to create any blog or personal portfolio. 

By accessing the Django Admin section, a user can easily manage the following website content such as:
- Articles 
- Sub-categories
- Categories

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

In order to faciliate testing and deployment tasks, a full CI/CD workflow has been implemented using Travis CLI, Ansible, and Docker/Kubernetes.


## Quick Start

### Prerequisites
Before building and running the application locally, your system must meet the following prerequisites :

1. Install dependencies
```
$ conda env create -f environment.yml
$ conda env activate portfolio
```

2. Set the following environment variables

|**Environment Variables**     |**Description**                                                  |
|------------------------------|------------------------------------------------------------------|
|`DEBUG`                       | Django variable in settings.py                                   |
|`SECRET_KEY`                  | Django variable in settings.py                                   |
|`EMAIL_HOST_USER`             | Email addr. for users to send messages (contact page) (optional) |
|`EMAIL_HOST_PASSWORD`         | Email address password (optional)                                |


3. Create a local Postgres database `portfoliodb`

### Running the app locally (dev/test)
Running the server locally without external docker services
```
$ make env-create
$ source .env
$ cd app
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

Note: The following services will not available during development (docker only)
- Celery
- Redis
- Nginx 


## Create Portfolio app image

### Create image
```
$ make portfolio
$ make latest
$ make up
$ make create-superuser
$ make down
```
Note: A Travis CLI workflow performs automatically the steps describe above, for every push to master.
- Test app source code with unit-tests
- Package app source code into a tarball (portfolio.tar.gz file)
- Build app image with latest tag
- Start services with docker-compose (App, Nginx, Celery, Redis, and Postgres)
- Check that all services are up and healthy
- Stop and remove services
- Publish image with latest tag to Dockerhub
- TO-DO: Front-end/integration tests

### Publish release image to Dockerhub
Prerequisites:
- Unit tests are passing
- A Docker image `${PORTFOLIO_IMAGE}:latest` has been create from `make latest`
- `make services-up` shows all services up and healthy 
- The following environment variables are set: `DOCKER_REGISTRY` (default to docker.io), `DOCKER_USER` and `DOCKER_PASSWORD`
To publish the portfolio image to a docker registry, run `make publish-latest` or `make publish-tagged`.



## Manual Deployment Options

### Deployment with docker-compose (dev/test)

### Deployment with Docker Swarm (prod)
```
$ cd deployment/
$ make stack-deploy
$ make watch-containers (separate terminal)
```

### Deployment with Kubernetes (prod)
```
$ kubect apply -f deployment/k8s-deployment
```

## Automated Deployment Options

### Ensure the Manager node instance is running:
```
$ cd cluster-management
$ make swarm-instance-start
```

### Docker Swarm deployment
```
$ cd cluster-management
$ make swarm-deployment-all
```
This command triggers an Ansible script to perform the following tasks:
- Install dependencies (eg. Docker, Docker-Compose, etc)
- Clone repo
- Prune all docker components
- Run stack deployment
- Check services are up and healthy

### Kubernetes deployment
```
$ cd cluster-management
$ make k8s-deployment-all
```
This command triggers an Ansible script to perform the following tasks:
- Install dependencies (eg. Docker, Docker-Compose, etc)
- Clone repo
- Prune all docker components
- Run kubernetes objects deployment
- Check services are up and healthy

## Backing up Postgres
This assume the postgres container is up and running on the docker swarm manager instance.
```
$ cd cluster-management
$ make swarm-backup-postgres
```


##### Potential improvements
- Use mongoDB to store image data
[![Travis Build Status](https://travis-ci.com/gbourniq/portfolio.svg?branch=master)](https://travis-ci.com/gbourniq/portfolio)



## Repository overview
This repository features of the following:
- Django web application which can be used as a template for a personal portfolio
- Instructions to set up the development environment with Conda, Poetry, and Makefiles
- Extensive documentation to easily deploy your own app on AWS EC2 with docker-compose (or Kubernetes/Helm - WIP)
- Integration features with AWS S3 to serve application files and backup Postgres data
- CI/CD pipeline with Travis CI and Ansible



## Contents
- [Portfolio application overview](#application-architecture)
- [Setting up the repository](#application-architecture)
- [Local development](#quick-start)
- [Docker deployment](#manual-deployment-options)
- [CI/CD pipeline](#automated-deployment-options)
- [Appendix: Environment variables](#backing-up-postgres)

## Portfolio Application overview
The portfolio app essentially displays "items" (or "articles"), which may include formatted text and media files. Those items can be  grouped into categories for a better navi. The application front-end is based on the [Materialize CSS](https://materializecss.com) framework. A sample app can be seen at htts://gbournique.com. 

<SCREENSHOT OF CATEGORY, HOMEPAGE, ITEMS?>



## Setting up the repository
- Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- Install [Poetry](https://github.com/sdispater/poetry) - you will need version 1.0.0 or greater
- Install [Make](https://www.gnu.org/software/make/) - to run command in Makefiles
- Clone this repo [portfolio] (https://github.com/gbourniq/portfolio.git) and cd into it

### 1. Creating the virtual environment
cd into portfolio root directory and source environment variables
```bash
cd portfolio
source .dev.env
```

To make things easy, we have added this to the Makefile, so you can create the conda environment and install the dependencies by simply running:

```bash
make env
```
Note: the environment can be rebuilt using the same command.

Activate the environment
```bash
conda activate portfolio
```

### 2. Set up git hooks
We use pre-commit (a pip package) to manage our git hooks. The hooks are defined in `.pre-commit-config.yaml`, and allows to automatically format the code with `isort` and `black`. To set them up, run:
```bash
make pre-commit
```

Alternatively the code can be manually linted using:
```bash
make lint-code
```
 

### 3. Install postgres

If it is not already installed, install [Postgres](https://www.postgresql.org/download/).

After installation, you may need to change some of the postgres configuration to open it up to allow connections from your services.

You can find the path to your postgres config files by running:

```bash
ps aux | grep 'postgres *-D'
```
If the above doesn’t work, enter the postgres shell and type:
```bash
SHOW config_file;
```

In *postgresql.conf*, change *#listen_addresses = ‘localhost’* to *listen_addresses = ‘*’* In *pg_hba.conf*, change the following lines: Change *127.0.0.1/32* to *0.0.0.0/0* and *::1/128* to *::/0*

Create airflow postgres database


### 4. Create portfoliodb database
Open a postgres shell as the root user:
```bash
psql
```
In the psql shell execute the following commands:
```bash
CREATE USER portfoliodb PASSWORD 'portfoliodb';
CREATE DATABASE portfoliodb;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO portfoliodb;
ALTER ROLE portfoliodb IN DATABASE portfoliodb SET search_path = portfoliodb,public;
```

### 5. Environment variables overview
Environment variables are located in two files: `deployment/.env` and `.dev.env`, and `deployment/.env` will automatically be sourced when `.dev.env` is sourced. 

`deployment/.env` contains variables required exclusively for deployment (prod build), and `.dev.env` adds variables for used development and the ci/cd pipeline (dev build).

![image](documentation/images/environment_variables.png)

Note that sourcing any `.env` file will automatically run the validation scripts `scripts/env_validation.sh` to ensure variables are set correctly. 

For example a warning will be raised if `AWS_ACCESS_KEY_ID` or `AWS_SECRET_ACCESS_KEY` are missing, while having `AWS_ENABLED=True`.

Both `.env` files allows to customise the dev/uat/prod experience such as:
- Run app with either local django server + postgres or docker-compose deployment (includes postgres, redis, celery)
- Building a custom app image and publishing to a personal private repository
- Use AWS S3 to store and serve Django media/static files
- Push artefacts to S3 such as Postgres dumps and docker deployment packages (tarballs)
- Use Ansible to automatically deploy application on AWS EC2 with docker-compose

The appendix [section]() #application-architecture include a list of all environment variables and a short description for each.


## Local Development

### Running the server locally without external docker services
Prerequisite: Postgres must be running locally

If not already active, activate the portfolio conda environment:
```bash
conda activate portfolio
```

Source environment variables for development
```bash
export BAREMETAL_DEPLOYMENT=True
cd portfolio/  # if not already at the root of the repository.
source .dev.env
cd app/
```
(TIP: autoenv is pretty nice to automate the activation of environments)

Alternativately `BAREMETAL_DEPLOYMENT` can be modified directly in `.dev.env`. Don't forget to source the file again after any change!

Create django superuser to access /admin page
```bash
python manage.py createsuperuser
```

Apply django model migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

Run the django server locally:
```bash
python manage.py runserver
```

### Wipe local Postgres database
If you want to wipe the database for whatever reason, run:
```bash
dropdb portfoliodb
createdb portfolio
```

Alternatively, we have a script to recreate a fresh database, apply migrations and create a default Django admin superuser:
```bash
make recreatedb
```

### Testing
To run the tests, run:

```bash
pytest -v
```

To check test coverage you can generate a coverage report (replace `--cov=.` with a specific directory for a more targeted report):

```bash
pytest --cov=. --cov-report=term-missing
```

### Versioning
The application versioning is based on the [Semantic Versioning 2.0.0](https://semver.org): <major.minor.patch>.  The version can be found in `pyproject.toml` and can be incremented with `poetry version {bump rule}`.
Valid bump rules are:
1. patch
2. minor
3. major
4. prepatch
5. preminor
6. premajor
7. prerelease

### Build and publish Docker image

Before building the image, set the image name in `deployment/.env`:
```
export IMAGE_REPOSITORY=<your-image-name>
```

Then make sure that `.dev.env` is sourced from the root of the repository
```bash
cd portfolio/  # if not already at the root of the repository.
source .dev.env
```

To build the image, the following command must be run from the */portfolio* root directory:
```bash
make image-latest
```
Alternatively the application version (set in `pyproject.toml`) can be used to tag the image:
```bash
make image-tagged
```

Note that the docker image build script will generate a `portfolio.tar.gz` in /bin. This tarball contains the application code that is copied into the image.
```
bin/portfolio.tar.gz
├── app
│   ├── main
│   ├── manage.py
│   ├── portfolio
│   ├── static
│   └── static_settings.py
└── scripts
    ├── check_services_health.sh
    ├── env_validation.sh
    ├── postgres_dump_to_s3.sh
    ├── postgres_restore_from_s3.sh
    └── reset_local_db.sh
```

The image can then be published using `make publish-latest` and `make publish-tagged`.

## Docker Deployment

### Docker Services Architecture
The application is composed of the following docker services:
- `Nginx` as a reverse proxy (prod build only)
- `Django web server` (dev/prod builds)
- `Celery` worker for asynchronous tasks (dev/prod builds)
- `Redis` as a message broker and caching (dev/prod builds)
- `Postgres` to store web server data (dev/prod builds)

These services are defined in `deployment/docker-deployment/*.docker-compose.yaml` files.

### Running the webserver with docker services (dev build)

The application can be run with docker-compose files, when `BAREMETAL_DEPLOYMENT` is set to `False` in `.dev.env`.
In addition to the Django webserver and Postgres (baremetal approach), the following services will be created:

Make sure that `.dev.env` is sourced, with `export BUILD=dev`
```bash
cd portfolio/  # if not already at the root of the repository.
source .dev.env
```

To start the docker-services, run:
```bash
make up
```
This will make the django webserver available at `localhost:8080`

To check that all services are up and healthy, run:
```bash
make check-services-health
```

Once the services are up, the Postgres backup script can be tested, given the following conditions are met:
- `AWS_ENABLE` set to *True*
- `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` are set
- An AWS S3 bucket has been created, and `AWS_STORAGE_BUCKET_NAME` / `AWS_DEFAULT_REGION` are set
Note: Instructions on how to set AWS S3 can be found in the extensive <deployment documentation>

The script will dump the Postgres data from the running container to S3, and then restore Postgres from the latest dump from on S3.
```bash
make postgres-backup-test
```

To delete all services, run:
```bash
make down
```

### Build the docker deployment artefact

In order to easily deploy the application to any new instance, one can generate a compressed folder (.tar.gz), which includes only the necessary file for a production deployment:
```
bin/docker_deploy.tar.gz
├── deployment
│   ├── .env
│   ├── Makefile
│   └── docker-deployment
│       ├── app
│       │   ├── prod.startup_server.sh
│       │   └── startup_celery.sh
│       ├── nginx
│       │   ├── certs
│       │   │   ├── cert_chain.crt
│       │   │   └── www_gbournique_com.key
│       │   └── conf.d
│       │       └── nginx.conf
│       ├── postgres
│       │   ├── config
│       │   │   └── postgres.conf
│       │   └── docker-entrypoint-initdb.d
│       │       └── run_db_setup.sh
│       ├── redis
│       │   └── redis_healthcheck.sh
│       └── prod.docker-compose.yml
└── scripts
    ├── check_services_health.sh
    ├── env_validation.sh
    ├── postgres_dump_to_s3.sh
    └── postgres_restore_from_s3.sh
```

This compressed folder is referred as the *docker deploy tarball*, and it can be generated by running:
```bash
make docker-deploy-tarball-custom
```
Note: by default this will generate `docker_deploy.tar.gz` file, but a custom file name can be specified with the `S3_DOCKER_DEPLOY_TARBALL_CUSTOM` environment variable.
Note2: The generated tarball will be automatically uploaded to S3, if AWS credentials are set and S3 bucket variables are configured.

### Running the server with docker services (prod)

The production deployment adds the `nginx` service as a reverse proxy (prod build only), and use a different startup script for the django webserver (using gunicorn).

To test the production deployment locally, run:
```bash
cd deployment
source .env
make up
```
The prod build deployment will not expose any development port, and incoming traffic is managed by nginx (80/443).

In practice, the prod build should be deployed on a remote instance using the *docker deploy tarball*.
Extensive instruction to deploy the app on AWS can be found in the <DEPLOYMENT> documentation.






## CI/CD Pipeline

In order to faciliate testing, build, and deployment tasks, a CI/CD workflow has been implemented using Travis CI.

![image](documentation/images/ci_cd_pipeline.png)

### CI Pipeline

The CI pipeline can triggered locally, by running a make command from the portfolio/ project root directory:
```bash
make run-ci-pipeline
```
This will trigger the following steps:
1. Create (or re-create) the conda environment and install dependencies from `poetry.lock`
2. Lint application code with `autoflake`, `isort` and `black`. Any linting error will cause the pipeline to fail.
3. Run unit-tests with pytest
Note: Any error such a linting error or failed tests will abort the pipeline.

### CD Pipeline

Similarly the CD pipeline can be triggered by running:
```bash
make run-cd-pipeline
```
This includes the following steps:
1. Package application code into /bin/portfolio.tar.gz and build docker image
2. Start docker services for the development build (without nginx)
3. Wait until all services are up and healthy
4. Test postgres backup scripts (only if S3 variables are configured): Dump pgdata to S3, then restore the latest dump from S3 
5. Stop and remove docker services for the development build
6. Publish docker portfolio app image (with the latest tag) to the online repository
7. Create docker deploy tarball, and upload to S3 (only if S3 configured)
8. Run Ansible playbook for an automated prod build deployment on AWS EC2 (if `RUN_ANSIBLE_PLAYBOOK=True`) 
Note: Any error in any step described above will cause the pipeline to fail.

### Ansible

The final step of the CD pipeline runs an Ansible playbook to ensure a smooth deployment on fresh EC2 instances. The Ansible playbook documentation can be found in `ansible/README.md`.

### Travis

This repository uses [Travis CI](https://travis-ci.org) to run the CI/CD pipeline (including the Ansible step) on Travis servers on every new commit to `master`. Travis CI is free when configured with public Github repositories.

The Travis building configuration file `.travis.yml` defines the following steps:
1. Install Docker / docker-compose
2. Install Miniconda
3. Install dependencies: make, sshpass
4. Run CI/CD pipeline with `make run-ci-cd-pipeline`

Note that the following environment variables must be set in the Travis build configuration settings, at https://travis-ci.com.
![image](documentation/images/travis_env_variables.png)





## Appendix: Environment variables

### Secret Environment variables:

The following variables must be defined on host (locally, and on Travis CI):

|**Name**                      |**Description**                                                               |
|------------------------------|------------------------------------------------------------------------------|
|`ANSIBLE_VAULT_PASSWORD`      | Passphrase used to encrypt/decrypt secret variables (see /ansible/README.md) |
|`ANSIBLE_SSH_PASSWORD`        | SSH password for ec2 instance (see documentation/ec2_deployment_guide.html)  |
|`AWS_ACCESS_KEY_ID`           | Programmatic access for AWS EC2 and S3 (see ec2_deployment_guide.html)       |
|`AWS_SECRET_ACCESS_KEY`       | Programmatic access for AWS EC2 and S3 (see ec2_deployment_guide.html)       |
|`DOCKER_USER`                 | Docker username to publish and pull portfolio app image                      |
|`DOCKER_PASSWORD`             | Docker password to publish and pull portfolio app image                      |
|`EMAIL_HOST_USER`             | Email addr. for website users to send messages via contact page (Optional)   |
|`EMAIL_HOST_PASSWORD`         | Email address password (Optional)                                            |


### Environment variables for deployment (prod build)

Main variables in `deployment/.env`:
* Secret variables that must be defined on host
* Django settings for prod build
* AWS variables to use Postgres backup scripts and serve django static/media files with S3
* Docker variables for publishing/pulling app image

|**Name**                      |**Description**                                                               |
|------------------------------|------------------------------------------------------------------------------|
|`BUILD`                       | Used by deployment scripts and ci-cd pipeline. Must be set to `prod`         |
|`DEBUG`                       | Should be set to False (production)                                          |
|`ALLOWED_HOSTS`               | Hosts names the Django site can serve to prevent HTTP Host header attacks    |
|`SECRET_KEY`                  | For a particular Django installation to provide cryptographic signing        |
|`ENABLE_S3_FOR_DJANGO_FILES`  | `True` for S3 to store and serve Django files, `False` to use Filesystem     |
|`POSTGRES_*`                  | Variables for Django app container to connect to Postgres container          |
|`REDIS_*`                     | Variables for Django app container to connect to the Redis container         |
|`AWS_ENABLED`                 | Must be set to `False` if AWS S3 is not used                                 |
|`AWS_DEFAULT_REGION`          | Region associated with the S3 bucket. eg. eu-west-2                          |
|`AWS_STORAGE_BUCKET_NAME`     | S3 bucket storing PG backups, django files, and docker deploy tarballs       |
|`IMAGE_REPOSITORY`            | Docker repository for the portfolio app image                                |

### Environment variables for development (dev build)

Main variables in `.dev.env`:
* Secret variables that must be defined on host
* General settings
* Django settings for dev build
* AWS S3 variables to upload docker deployment tarball
* Ansible variables (Not used if `RUN_ANSIBLE_PLAYBOOK=False`)


|**Name**                      |**Description**                                                               |
|------------------------------|------------------------------------------------------------------------------|
|`BUILD`                       | Used by deployment scripts and ci-cd pipeline. Must be set to `dev`          |
|`BAREMETAL_DEPLOYMENT`        | `True` to run django server locally, and `False` for any docker deployment   |
|`RUN_ANSIBLE_PLAYBOOK`        | Set to `False` to skip the Ansible playbook in the CD pipeline               |
|`CONDA_ENV_NAME`              | Name of the conda environment. `portfolio` is the default name               |
|`DEBUG`                       | Set to `True` to see detailed logs during development                        |
|`ENABLE_S3_FOR_DJANGO_FILES`  | Can be set to `False` to prevent Django using S3 for media/static files      |
|`DOCKER_DEPLOY_FOLDER`        | Folder in `AWS_STORAGE_BUCKET_NAME` to store docker deploy tarballs          |
|`S3_DOCKER_DEPLOY_CD_PIPELINE`| Basename of docker deployment tarball used by ci/cd pipeline and Ansible     |
|`S3_DOCKER_DEPLOY_CUSTOM`     | Basename of docker deployment tarball used by user to manually deploy app    |
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



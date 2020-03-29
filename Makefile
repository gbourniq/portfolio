# Set shell
SHELL=/bin/bash -e -o pipefail

# Cosmetics
RED := "\e[1;31m"
YELLOW := "\e[1;33m"
GREEN := "\033[32m"
NC := "\e[0m"
INFO := @bash -c 'printf ${YELLOW}; echo "[INFO] $$1"; printf ${NC}' MESSAGE
MESSAGE := @bash -c 'printf ${NC}; echo "$$1"; printf ${NC}' MESSAGE
SUCCESS := @bash -c 'printf ${GREEN}; echo "[SUCCESS] $$1"; printf ${NC}' MESSAGE
WARNING := @bash -c 'printf ${RED}; echo "[WARNING] $$1"; printf ${NC}' MESSAGE

# Conda environment
CONDA_ENV_NAME=portfolio
CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh; conda activate ${CONDA_ENV_NAME}

# Docker
PORTFOLIO_DOCKERFILE=deployment/docker-build/app.Dockerfile
PROJECT_NAME=portfolio
COMPOSE_FILE=docker-compose.yml
COMPOSE_ARGS="-p ${PROJECT_NAME} -f ${COMPOSE_FILE}"
POETRY_VERSION=1.0.5

### INSTALL DEPENDENCIES ###
.PHONY: env
env:
	${INFO} "Creating conda environment and installing poetry packages"
	@ conda env create
	${SUCCESS} "${CONDA_ENV_NAMEm} conda environment has been created!"
	@ ($(CONDA_ACTIVATE); poetry install)
	${SUCCESS} "Dependencies installed with Poetry!"
	${MESSAGE} "Please activate the conda environment and source your environment variables:"
	${MESSAGE} "- conda activate ${CONDA_ENV_NAME}"
	${MESSAGE} "- source .env"

### SET PRE-COMMIT ###
.PHONY: pre-commit
pre-commit:
	@ pre-commit install -t pre-commit -t commit-msg
	${SUCCESS} "pre-commit set up"

### UNIT TESTS ###
.PHONY: unit-tests
unit-tests: 
	${INFO} "Running unit tests"
	@ cd app; pytest .
	
### PACKAGE APPLICATION ###
.PHONY: portfolio
portfolio:
	${INFO} "Building portfolio package"
	python utils/builder.py --name ${PROJECT_NAME}

### DOCKER BUILD ###
.PHONY: tagged-image
tagged-image:
	${INFO} "Building docker image ${IMAGE_REPOSITORY}:${IMAGE_TAG}"
	@ docker build -f ${PORTFOLIO_DOCKERFILE} -t ${IMAGE_REPOSITORY}:${IMAGE_TAG} \
		--build-arg PORTFOLIO_TARBALL=./bin/portfolio.tar.gz . \
		--build-arg POETRY_VERSION=${POETRY_VERSION} \
		--build-arg POETRY_LOCK_FILE=./poetry.lock \
		--build-arg PYPROJECT_FILE=./pyproject.toml \
		--build-arg CELERY_STARTUP=./deployment/docker-build/startup_celery.sh \
		--build-arg SERVER_STARTUP=./deployment/docker-build/startup_server.sh
	${SUCCESS} "${IMAGE_REPOSITORY}:${IMAGE_TAG} built successfully"

.PHONY: latest
latest:
	${INFO} "Building docker image ${IMAGE_REPOSITORY}:latest"
	@ docker build -f ${PORTFOLIO_DOCKERFILE} -t ${IMAGE_REPOSITORY}:latest \
		--build-arg PORTFOLIO_TARBALL=./bin/portfolio.tar.gz . \
		--build-arg POETRY_VERSION=${POETRY_VERSION} \
		--build-arg POETRY_LOCK_FILE=./poetry.lock \
		--build-arg PYPROJECT_FILE=./pyproject.toml \
		--build-arg CELERY_STARTUP=./deployment/docker-build/startup_celery.sh \
		--build-arg SERVER_STARTUP=./deployment/docker-build/startup_server.sh
	${SUCCESS} "${IMAGE_REPOSITORY}:latest built successfully"

### DOCKER COMPOSE ###
.PHONY: up
up:
	${INFO} "Starting docker-compose services using ${IMAGE_REPOSITORY}:latest..."
	@ cd deployment/docker-deployment && docker-compose ${COMPOSE_ARGS} up -d
	${SUCCESS} "Services started successfully"
	${INFO} "Checking services health..."
	@ cd deployment/docker-deployment && $(call check_service_health,${COMPOSE_ARGS},postgres)
	${MESSAGE} "POSTGRES OK."
	@ cd deployment/docker-deployment && $(call check_service_health,${COMPOSE_ARGS},redis)
	${MESSAGE} "REDIS OK."
	@ cd deployment/docker-deployment && $(call check_service_health,${COMPOSE_ARGS},app)
	${MESSAGE} "WEB SERVER OK."
	@ cd deployment/docker-deployment && $(call check_service_health,${COMPOSE_ARGS},worker)
	${MESSAGE} "CELERY WORKER OK."
	${SUCCESS} "All services are healthy"

.PHONY: down
down:
	${INFO} "Removing docker-compose services..."
	@ cd deployment/docker-deployment && docker-compose ${COMPOSE_ARGS} down --remove-orphans
	${SUCCESS} "Services removed successfully"

.PHONY: stop
stop:
	${INFO} "Stopping docker-compose services..."
	@ cd deployment/docker-deployment && docker-compose ${COMPOSE_ARGS} stop
	${SUCCESS} "Services stopped successfully"

### PUBLISH IMAGE ###
.PHONY: docker-login
docker-login:
	@ docker login ${DOCKER_REGISTRY} -u ${DOCKER_USER} -p ${DOCKER_PASSWORD}

.PHONY: publish-tagged
publish-tagged: docker-login
	${INFO} "Publishing ${IMAGE_REPOSITORY}:${IMAGE_TAG} image to Dockerhub..."
	@ docker push ${IMAGE_REPOSITORY}:${IMAGE_TAG}
	${SUCCESS} "Image published successfully"

.PHONY: publish-latest
publish-latest: docker-login
	${INFO} "Publishing ${IMAGE_REPOSITORY}:latest image to ${DOCKER_REGISTRY:-docker.io}..."
	@ docker push ${IMAGE_REPOSITORY}:latest
	${SUCCESS} "Image published successfully"

### CREATE DJANGO SUPERUSER ###
.PHONY: create-superuser
create-superuser:
	${INFO} "Creating initial temporary superuser: username: admin, password: admin..."
	@ echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | docker exec -i app python app/manage.py shell
	${SUCCESS} "Superuser created"


###### FUNCTIONS ######

# Service health functions
# Syntax: $(call check_service_health,<docker-compose-environment>,<service-name>)
get_container_id = $$(docker-compose $(1) ps -q $(2))
get_container_state = $$(echo $(call get_container_id,$(1),$(2)) | xargs -I ID docker inspect -f '$(3)' ID)
get_service_health = $$(echo $(call get_container_state,$(1),$(2),{{if .State.Running}}{{ .State.Health.Status }}{{end}}))
check_service_health = { \
  until [[ $(call get_service_health,$(1),$(2)) != starting ]]; \
    do sleep 1; \
  done; \
  if [[ $(call get_service_health,$(1),$(2)) != healthy ]]; \
    then echo $(2) failed health check; exit 1; \
  fi; \
}
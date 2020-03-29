# Set shell
SHELL=/bin/bash -e -o pipefail

# Cosmetics
RED := "\e[1;31m"
YELLOW := "\e[1;33m"
GREEN := "\033[32m"
NC := "\e[0m"
INFO := @bash -c 'printf $(YELLOW); echo "[INFO] $$1"; printf $(NC)' MESSAGE
MESSAGE := @bash -c 'printf $(NC); echo "$$1"; printf $(NC)' MESSAGE
SUCCESS := @bash -c 'printf $(GREEN); echo "[SUCCESS] $$1"; printf $(NC)' MESSAGE
WARNING := @bash -c 'printf $(RED); echo "[WARNING] $$1"; printf $(NC)' MESSAGE

ENVIRONMENT_NAME=portfolio
PORTFOLIO_DOCKERFILE=deployment/docker-build/app.Dockerfile
PROJECT_NAME=portfolio
COMPOSE_FILE=docker-compose.yml
COMPOSE_ARGS = -p $(PROJECT_NAME) -f $(COMPOSE_FILE)
POETRY_VERSION=1.0.5

### REPO ###
.PHONY: pre-commit
pre-commit:
	@pre-commit install -t pre-commit -t commit-msg
	${SUCCESS} "pre-commit installed"


### CONDA AND POETRY ###
.PHONY: env-create
env-create:
	${INFO} "Creating conda environment and running `poetry install`"
	@conda env create
	@conda activate ${ENVIRONMENT_NAME}
	@poetry install
	${SUCCESS} "Success"

### PACKAGE ###
.PHONY: portfolio
portfolio:
	${INFO} "Building portfolio package"
	python utils/builder.py --name ${ENVIRONMENT_NAME}

### DOCKER ###
.PHONY: latest
latest:
	${INFO} "Building docker image ${PORTFOLIO_IMAGE}:latest"
	@ docker build -f $(PORTFOLIO_DOCKERFILE) -t ${PORTFOLIO_IMAGE} \
		--build-arg PORTFOLIO_TARBALL=./bin/portfolio.tar.gz . \
		--build-arg POETRY_VERSION=$(POETRY_VERSION) \
		--build-arg POETRY_LOCK_FILE=./poetry.lock \
		--build-arg PYPROJECT_FILE=./pyproject.toml \
		--build-arg CELERY_STARTUP=./deployment/docker-build/startup_celery.sh \
		--build-arg SERVER_STARTUP=./deployment/docker-build/startup_server.sh

	# @echo 'y' | docker image prune
	${SUCCESS} "${PORTFOLIO_IMAGE}:latest built successfully"

### DOCKER COMPOSE ###
.PHONY: services-up
services-up:
	${INFO} "Starting docker-compose services..."
	@ cd deployment/docker-deployment && docker-compose $(COMPOSE_ARGS) up -d
	${SUCCESS} "Services started successfully"
	${INFO} "Checking services health..."
	@ cd deployment/docker-deployment && $(call check_service_health,$(COMPOSE_ARGS),postgres)
	${MESSAGE} "POSTGRES OK."
	@ cd deployment/docker-deployment && $(call check_service_health,$(COMPOSE_ARGS),redis)
	${MESSAGE} "REDIS OK."
	@ cd deployment/docker-deployment && $(call check_service_health,$(COMPOSE_ARGS),app)
	${MESSAGE} "WEB SERVER OK."
	@ cd deployment/docker-deployment && $(call check_service_health,$(COMPOSE_ARGS),worker)
	${MESSAGE} "CELERY WORKER OK."
	${SUCCESS} "All services are healthy"

# Superuser to be created the first time the app is deployed via docker-compose (fresh PostgreSQL)
.PHONY: create-superuser
create-superuser:
	${INFO} "Creating initial temporary superuser: username: admin, password: admin..."
	@ echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | docker exec -i app python app/manage.py shell
	${SUCCESS} "Superuser created"

.PHONY: services-down
services-down:
	${INFO} "Stopping and removing docker-compose services..."
	@ cd deployment/docker-deployment && docker-compose $(COMPOSE_ARGS) down --remove-orphans
	${SUCCESS} "Services removed successfully"




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
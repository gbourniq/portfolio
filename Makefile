# Set shell
SHELL=/bin/bash -e -o pipefail

# Cosmetics
RED := "\e[1;31m"
YELLOW := "\e[1;33m"
GREEN := "\033[32m"
NC := "\e[0m"
INFO := @bash -c 'printf $(YELLOW); echo "[INFO] $$1"; printf $(NC)' MESSAGE
INSTRUCTION := @bash -c 'printf $(NC); echo "   $$1"; printf $(NC)' MESSAGE
SUCCESS := @bash -c 'printf $(GREEN); echo "[SUCCESS] $$1"; printf $(NC)' MESSAGE
WARNING := @bash -c 'printf $(RED); echo "[WARNING] $$1"; printf $(NC)' MESSAGE

IMAGE=docker.io/gbournique/myportfolio_app
ENVIRONMENT_NAME=portfolio
PROJECT_NAME=portfolio
PORTFOLIO_DOCKERFILE=deployment/docker-build/app.Dockerfile
COMPOSE_FILE=deployment/docker-deployment/docker-compose.yml
COMPOSE_ARGS = -p $(PROJECT_NAME) -f $(COMPOSE_FILE)

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

.PHONY: env-activate-local
env-activate-local:
	@source app/.env
	${SUCCESS} "Sourced environment variables for local development"

.PHONY: env-activate-docker
env-activate-docker:
	@source deployment/docker-deployment/.env
	${SUCCESS} "Sourced environment variables for docker deployment"

### PACKAGE ###
.PHONY: portfolio
portfolio:
	${INFO} "Building portfolio package"
	python helpers/builder.py --name ${ENVIRONMENT_NAME}

### DOCKER ###
.PHONY: latest
latest:
	${INFO} "Building docker image ${IMAGE}:latest"
	@docker build -f $(PORTFOLIO_DOCKERFILE) -t ${IMAGE} --build-arg PORTFOLIO_TARBALL=./bin/portfolio.tar.gz .
	# @echo 'y' | docker image prune
	${SUCCESS} "${IMAGE}:latest built successfully"

### DOCKER COMPOSE ###
.PHONY: services-up
services-up:
	${INFO} "Starting docker-compose services..."
	@ docker-compose $(COMPOSE_ARGS) up -d
	${SUCCESS} "Services started successfully"
	${INFO} "Checking services health..."
	@ $(call check_service_health,$(COMPOSE_ARGS),postgres)
	@ $(call check_service_health,$(COMPOSE_ARGS),redis)
	@ $(call check_service_health,$(COMPOSE_ARGS),app)
	@ $(call check_service_health,$(COMPOSE_ARGS),worker)
	@ $(call check_service_health,$(COMPOSE_ARGS),nginx)
	${SUCCESS} "All services are healthy"
	${SUCCESS} "Client REST endpoint is running with NGINX at http://$(DOCKER_HOST_IP):443"

# Superuser to be created the first time the app is deployed via docker-compose (fresh PostgreSQL)
.PHONY: create-superuser
create-superuser:
	${INFO} "Creating initial temporary superuser: username: admin, password: pass..."
	@ echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | docker exec -i app python manage.py shell
	${SUCCESS} "Superuser created"

.PHONY: services-down
services-down:
	${INFO} "Stopping and removing docker-compose services..."
	@ docker-compose $(COMPOSE_ARGS) down --remove-orphans
	${SUCCESS} "Services removed successfully"


### DOCKER STACK ###
# stack-deploy:
# 	${INFO} "Deploying stack..."
# 	@ docker stack deploy -c docker-deployment/stack.yml myportfolio
# 	${SUCCESS} "Stack deployment complete..."

# stack-rm:
# 	${INFO} "Removing stack..."
# 	@ docker stack rm myportfolio || true 
# 	${SUCCESS} "Stack remove complete..."

# watch-containers:
# 	${INFO} "Watch containers lifecycle..."
# 	@ watch -n 2 'docker ps --format "table {{.ID}}\t {{.Image}}\t {{.Status}}"'


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
SHELL := /bin/bash

# Include env variables
# include .env
# Common settings
include Makefile.settings

# Executes a full workflow
rebuild-app-image: remove-app-image clean-environment build-app-image
publish-app-image: remove-app-image clean-environment build-app-image tag/latest publish/latest
deploy-compose: services-down clean-environment services-up
swarm-all: services-down clean-environment stack-rm stack-deploy

# Login to Docker registry
login-ask-cli:
	${INFO} "Logging in to Docker registry $(DOCKER_REGISTRY)..."
	@ docker login -u $(DOCKER_USER) -p $(DOCKER_PASSWORD_CLI)
	${SUCCESS} "Logged in to Docker registry $(DOCKER_REGISTRY)"

# Login to Docker registry
login:
	${INFO} "Logging in to Docker registry $(DOCKER_REGISTRY)..."
	@ docker login -u $(DOCKER_USER) -p $(DOCKER_PASSWORD)
	${SUCCESS} "Logged in to Docker registry $(DOCKER_REGISTRY)"

# Logout of Docker registry
logout:
	${INFO} "Logging out of Docker registry $(DOCKER_REGISTRY)..."
	@ docker logout
	${SUCCESS} "Logged out of Docker registry $(DOCKER_REGISTRY)"

# Superuser to be create the first time the app is deployed via docker-compose (fresh PostgreSQL)
create-superuser:
	${INFO} "Creating initial temporary superuser: username: admin, password: pass..."
	@ echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | docker exec -i app python manage.py shell
	${SUCCESS} "Superuser created"

clean-environment:
	${INFO} "Removing dangling images..."
	@ $(call clean_dangling_images,$(PROJECT_NAME))
	${SUCCESS} "Clean up complete"

build-app-image:
	${INFO} "Building app image..."
	@ docker-compose $(BUILD_ARGS) build
	${SUCCESS} "Image build complete"

unit-tests:
	${INFO} "Running unit tests..."
	@ docker run -it myportfolio_app:latest pytest .
	${SUCCESS} "Unit tests complete"

prune-all:
	${INFO} "Remove images starting with $(PROJECT_NAME)..."
	@ docker system prune -a -f 2>/dev/null || true
	${SUCCESS} "Images removed successfully"
	
services-up:
	${INFO} "Starting services for build environment..."
	@ docker-compose $(BUILD_ARGS) up -d
	${SUCCESS} "Production environment created"
	${SUCCESS} "Client REST endpoint is running with NGINX at http://$(DOCKER_HOST_IP):$(call get_port_mapping,$(BUILD_ARGS),nginx,443)"

services-down:
	${INFO} "Destroying build environment..."
	@ docker-compose $(BUILD_ARGS) down
	${SUCCESS} "Removed images and volumes for prod environment"

services-health:
	${INFO} "Checking services health..."
	@ $(call check_service_health,$(BUILD_ARGS),postgres)
	@ $(call check_service_health,$(BUILD_ARGS),redis)
	@ $(call check_service_health,$(BUILD_ARGS),app)
	@ $(call check_service_health,$(BUILD_ARGS),worker)
	@ $(call check_service_health,$(BUILD_ARGS),nginx)
	${SUCCESS} "All services are healthy"

frontend-tests:
	${INFO} "Running front-end tests..."
	@ echo "Front-end tests under progress..."
	${SUCCESS} "Front-end tests complete"

tag/%:
	${INFO} "Tagging release images with tags $*..."
	docker tag $(PROJECT_NAME)_app $(DOCKER_REGISTRY)/$(DOCKER_USER)/$(PROJECT_NAME)_app:$*
	${SUCCESS} "Tagging complete"

publish/%::
	${INFO} "Publishing release images with tags $* to $(DOCKER_REGISTRY)/$(DOCKER_USER)..."
	docker push $(DOCKER_REGISTRY)/$(DOCKER_USER)/$(PROJECT_NAME)_app:$*
	${SUCCESS} "Publishing complete"

stack-deploy:
	${INFO} "Deploying stack..."
	@ docker stack deploy -c docker-deployment/stack.yml myportfolio
	${SUCCESS} "Stack deployment complete..."

stack-rm:
	${INFO} "Removing stack..."
	@ docker stack rm myportfolio || true 
	${SUCCESS} "Stack remove complete..."

watch-containers:
	${INFO} "Watch containers lifecycle..."
	@ watch -n 2 'docker ps --format "table {{.ID}}\t {{.Image}}\t {{.Status}}"'


# error Error starting userland proxy: listen tcp 0.0.0.0:80: bind: address already in use
# sudo lsof -nP | grep LISTEN
# sudo kill -9 1548

# postgres-backup:
# 	${INFO} "Backing up PostgreSQL data to S3"
# 	@ cd ../cluster-management/utils && bash backup-postgres.sh
# 	${SUCCESS} "Backup complete..."

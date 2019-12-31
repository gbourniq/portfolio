SHELL := /bin/bash

# Include env variables
include .env
# Common settings
include Makefile.settings

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

test:
	${INFO} "Running tests..."
	# Run unit tests
	echo $(ls)

# Superuser to be create the first time the app is deployed (fresh PostgreSQL)
create-superuser:
	${INFO} "Creating superuser..."
	@ docker exec -it $(APP_CONTAINER_ID) python manage.py createsuperuser

# Executes a full workflow
docker-all: clean-environments test build-images services-up-build services-health services-down-volumes clean-environments

build-images:
	${INFO} "Building images..."
	@ docker-compose $(BUILD_ARGS) build
	${SUCCESS} "Images build complete"

clean-environments: remove-build-images
	${INFO} "Removing dangling images..."
	@ $(call clean_dangling_images,$(PROJECT_NAME))
	${SUCCESS} "Clean up complete"
	
remove-build-images:
	${INFO} "Remove images starting with $(PROJECT_NAME)..."
	@ docker rmi $(IMAGES_IDS) --force || true 
	${SUCCESS} "Images removed successfully"

services-up-build:
	${INFO} "Starting services for build environment..."
	@ docker-compose $(BUILD_ARGS) up -d
	${SUCCESS} "Build environment created"
	${SUCCESS} "Client REST endpoint is running with NGINX at http://$(DOCKER_HOST_IP):$(call get_port_mapping,$(BUILD_ARGS),nginx,$(PROXY_PORT_INTERNAL))" || true

services-up-prod:
	${INFO} "Starting services for production environment..."
	@ docker-compose $(PROD_ARGS) up -d
	${SUCCESS} "Production environment created"
	${SUCCESS} "Client REST endpoint is running with NGINX at http://$(DOCKER_HOST_IP):$(call get_port_mapping,$(BUILD_ARGS),nginx,$(PROXY_PORT_INTERNAL))"

services-down:
	${INFO} "Destroying build environment excluding volumes..."
	@ docker-compose $(BUILD_ARGS) down
	${SUCCESS} "Removed images and volumes for build environment"

services-down-volumes:
	${INFO} "Destroying build environment including volumes..."
	@ docker-compose $(BUILD_ARGS) down -v
	${SUCCESS} "Removed images and volumes for prod environment"

services-health:
	${INFO} "Checking services health..."
	@ $(call check_service_health,$(BUILD_ARGS),postgres)
	@ $(call check_service_health,$(BUILD_ARGS),redis)
	@ $(call check_service_health,$(BUILD_ARGS),app)
	@ $(call check_service_health,$(BUILD_ARGS),celery)
	@ $(call check_service_health,$(BUILD_ARGS),nginx)
	${SUCCESS} "All services are healthy"

tag/%:
	${INFO} "Tagging release images with tags $*..."
	docker tag $(PROJECT_NAME)_app $(DOCKER_REGISTRY)/$(ORG_NAME)/$(PROJECT_NAME)_app:$*
	docker tag $(PROJECT_NAME)_celery $(DOCKER_REGISTRY)/$(ORG_NAME)/$(PROJECT_NAME)_celery:$*
	docker tag $(PROJECT_NAME)_postgres $(DOCKER_REGISTRY)/$(ORG_NAME)/$(PROJECT_NAME)_postgres:$*
	docker tag $(PROJECT_NAME)_nginx $(DOCKER_REGISTRY)/$(ORG_NAME)/$(PROJECT_NAME)_nginx:$*
	docker tag $(PROJECT_NAME)_redis $(DOCKER_REGISTRY)/$(ORG_NAME)/$(PROJECT_NAME)_redis:$*
	${SUCCESS} "Tagging complete"

publish/%::
	${INFO} "Publishing release images with tags $* to $(DOCKER_REGISTRY)/$(ORG_NAME)..."
	docker push $(DOCKER_REGISTRY)/$(ORG_NAME)/$(PROJECT_NAME)_app:$*
	docker push $(DOCKER_REGISTRY)/$(ORG_NAME)/$(PROJECT_NAME)_celery:$*
	docker push $(DOCKER_REGISTRY)/$(ORG_NAME)/$(PROJECT_NAME)_postgres:$*
	docker push $(DOCKER_REGISTRY)/$(ORG_NAME)/$(PROJECT_NAME)_nginx:$*
	docker push $(DOCKER_REGISTRY)/$(ORG_NAME)/$(PROJECT_NAME)_redis:$*
	${SUCCESS} "Publishing complete"

stack-deploy:
	@ docker stack deploy -c docker-deployment/stack-app.yml myportfolio

stack-show-logs:



# IMPORTANT - ensures arguments are not interpreted as make targets
# %:
# 	@:
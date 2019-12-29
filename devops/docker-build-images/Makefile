DEPLOY_DIR=docker-build-images
ANSIBLE_DIR=ec2-deployment
SHELL := /bin/bash





# create super user - use existing logic automatically get the right container id?
# docker exec -it 120f5edfb608 python manage.py createsuperuser

# docker compose update
# docker-compose down && docker-compose build && docker-compose up



# Include env variables
include .env
# Common settings
include Makefile.settings


# Repo variables, eg. full image name: myfullstackapp_mongo:latest
REPO_NAME_BASE=myfullstackapp

# Prints version
docker-app-version:
	${INFO} "App version:"
	@ echo $(APP_VERSION)

# Login to Docker registry
docker-login/%:
	${INFO} "Logging in to Docker registry $(DOCKER_REGISTRY)..."
	@ docker login -u $(DOCKER_USER) -p $*
	${SUCCESS} "Logged in to Docker registry $(DOCKER_REGISTRY)"

# Logout of Docker registry
docker-logout:
	${INFO} "Logging out of Docker registry $(DOCKER_REGISTRY)..."
	@ docker logout
	${SUCCESS} "Logged out of Docker registry $(DOCKER_REGISTRY)"

docker-test:
	${INFO} "Running tests..."
	# Run unit tests
	cd .. && pytest .

# Executes a full workflow
docker-all: docker-clean docker-test docker-build-images docker-tag-latest docker-publish docker-clean

docker-build-images:
	${INFO} "Building images..."
	@ docker-compose $(BUILD_ARGS) build
	${SUCCESS} "Images build complete"

docker-start-services:
	${INFO} "Starting services for build environment..."
	@ docker-compose $(BUILD_ARGS) up -d
	${SUCCESS} "Build environment created"
	${SUCCESS} "App REST endpoint is running at http://$(DOCKER_HOST_IP):$(call get_port_mapping,$(BUILD_ARGS),app,$(APP_HTTP_PORT))$(APP_HTTP_ROOT)"
	${SUCCESS} "Client REST endpoint is running at http://$(DOCKER_HOST_IP):$(call get_port_mapping,$(BUILD_ARGS),client,$(CLIENT_HTTP_PORT))$(CLIENT_HTTP_ROOT)"

docker-start-services:
	${INFO} "Checking services health..."
	@ $(call check_service_health,$(BUILD_ARGS),mongo)
	@ $(call check_service_health,$(BUILD_ARGS),app)
	@ $(call check_service_health,$(BUILD_ARGS),client)
	${SUCCESS} "All services are healthy"


# Cleans environment
docker-clean:
	${INFO} "Removing dangling images..."
	@ $(call clean_dangling_images,$(REPO_NAME))
	${SUCCESS} "Clean up complete"

docker-down:
	${INFO} "Destroying build environment..."
	@ docker-compose $(BUILD_ARGS) down -v || true


# 'make tag <tag> [<tag>...]' tags development and/or release image with specified tag(s)
docker-tag/%:
	${INFO} "Tagging release images with tags $*..."
	docker tag $(PROJECT_NAME)_app $(DOCKER_REGISTRY)/$(ORG_NAME)/$(REPO_NAME_BASE)_app:$*
	docker tag $(PROJECT_NAME)_client $(DOCKER_REGISTRY)/$(ORG_NAME)/$(REPO_NAME_BASE)_client:$*
	${SUCCESS} "Tagging complete"

# Publishes image(s) tagged using make tag commands
docker-publish:
	${INFO} "Publishing release images to $(DOCKER_REGISTRY)/$(ORG_NAME)..."
	@ $(call publish_image,$(BUILD_ARGS),app,$(DOCKER_REGISTRY)/$(ORG_NAME)/$(REPO_NAME_BASE)_app)
	@ $(call publish_image,$(BUILD_ARGS),client,$(DOCKER_REGISTRY)/$(ORG_NAME)/$(REPO_NAME_BASE)_client)
	@ $(call publish_image,$(BUILD_ARGS),mongo,$(DOCKER_REGISTRY)/$(ORG_NAME)/$(REPO_NAME_BASE)_mongo)
	${SUCCESS} "Publish complete"

# IMPORTANT - ensures arguments are not interpreted as make targets
%:
	@:
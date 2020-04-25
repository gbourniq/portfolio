#!/bin/bash

INFO "Packaging portfolio app to /bin"
python utils/package_builder.py --name ${PROJECT_NAME}

INFO "Building docker image ${IMAGE_REPOSITORY}:latest"
docker build -f ${DOCKERFILE_PATH} -t ${IMAGE_REPOSITORY}:latest \
		--build-arg DOCKER_PORTFOLIO_HOME=${DOCKER_PORTFOLIO_HOME} \
		--build-arg DOCKER_APP_CODE=${DOCKER_APP_CODE} \
		--build-arg PORTFOLIO_TARBALL=./bin/portfolio.tar.gz . \
		--build-arg POETRY_VERSION=${POETRY_VERSION} \
		--build-arg POETRY_LOCK_FILE=./poetry.lock \
		--build-arg PYPROJECT_FILE=./pyproject.toml

SUCCESS "${IMAGE_REPOSITORY}:latest built successfully"
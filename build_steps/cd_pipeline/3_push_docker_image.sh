#!/bin/bash

# DOCKER_TAG_LATEST="latest"
# DOCKER_TAG_CURRENT=$(poetry version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+(?:-rc\.[0-9]+)?$')
# echo $DOCKER_TAG_CURRENT

# docker system prune -a --force

# # # Building docker image
# docker build -f docker_deployment/mvp.Dockerfile -t mvpipeline --build-arg MVP_TARBALL=bin/installer/mvp.tar.gz --build-arg CONDA_TARBALL=bin/installer/conda.tar.gz .

# # Logging in before pushing to dockerhub
# echo "$DOCKER_PASSWORD" | docker login --username "$DOCKER_USERNAME" --password-stdin

# # # Pushing latest to dockerhub
# docker tag mvpipeline eigentech/mvpipeline:${DOCKER_TAG_LATEST}
# docker push eigentech/mvpipeline:${DOCKER_TAG_LATEST}

# # # Logout
# docker logout

  - make docker-login
  - make publish-latest
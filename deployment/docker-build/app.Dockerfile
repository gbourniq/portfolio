FROM python:3.8-slim-buster as base_build

LABEL author="Guillaume Bournique <gbournique@gmail.com>"

ARG DOCKER_PORTFOLIO_HOME
ARG DOCKER_APP_CODE
ENV HOME="/home" \
    PORTFOLIO_HOME=${DOCKER_PORTFOLIO_HOME} \
    APP_CODE=${DOCKER_APP_CODE} \
    PYTHONPATH=${PORTFOLIO_HOME}

# Add additional basic packages.
# * gcc libpq-dev python3-dev: psycopg2 source dependencies
# * curl: to healthcheck services with http response
# * vim: Because it's awesome?
# * procps: useful utilities such as ps, top, vmstat, pgrep,...
# Clean the apt cache
RUN apt-get update \
    && apt-get install -yq --no-install-recommends gcc libpq-dev python3-dev curl vim procps \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
ARG USERNAME="app_user"
RUN adduser --disabled-password --gecos "" $USERNAME \ 
    && usermod -o -u 0 $USERNAME
# Sets default user for docker containers
USER $USERNAME

# Set work directory
WORKDIR ${PORTFOLIO_HOME}

# Copy dependencies files
ARG POETRY_LOCK_FILE
ARG PYPROJECT_FILE
COPY $POETRY_LOCK_FILE $PYPROJECT_FILE ./

# Install Poetry and project dependencies
ARG POETRY_VERSION
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Add project source code
ARG PORTFOLIO_TARBALL
ADD $PORTFOLIO_TARBALL ${HOME}

# Informs Docker that the container listens on 8000 at runtime
EXPOSE 8080

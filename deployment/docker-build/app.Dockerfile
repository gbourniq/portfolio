FROM python:3.8-slim-buster as base_build

LABEL author="Guillaume Bournique <gbournique@gmail.com>"

# ARG USERNAME="app_user"

ENV HOME="/home" \
    PORTFOLIO_HOME="/home/portfolio" \
    APP_CODE="/home/portfolio/app" \
    PYTHONPATH=${PORTFOLIO_HOME}

# Set work directory
WORKDIR ${PORTFOLIO_HOME}

# Add additional basic packages.
# * gcc libpq-dev python3-dev: psycopg2 source dependencies
# * curl: to healthcheck services with http response
# * vim: Because it's awesome?
# Clean the apt cache
# Create non-root user
RUN apt-get update \
    && apt-get install -yq --no-install-recommends gcc libpq-dev python3-dev curl vim \
    && rm -rf /var/lib/apt/lists/*
    # && adduser --disabled-password --gecos "" $USERNAME

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

# Add image entrypoints
ARG CELERY_STARTUP
ARG SERVER_STARTUP
COPY $CELERY_STARTUP $SERVER_STARTUP ${APP_CODE}/
RUN chmod +x ${APP_CODE}/startup_celery.sh ${APP_CODE}/startup_server.sh

# Sets default user for docker containers
# USER $USERNAME app_userapp_user

# Informs Docker that the container listens on 8000 at runtime
EXPOSE 8080

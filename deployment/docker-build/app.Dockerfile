FROM python:3.8-slim-buster as base_build

LABEL author="Guillaume Bournique <gbournique@gmail.com>"

ARG USERNAME="portfoliouser"
ENV PORTFOLIO_HOME="/home/${USERNAME}" \
    PYTHONPATH=${PORTFOLIO_HOME} \
    USERNAME=${USERNAME}

# Add additional basic packages.
# * gcc libpq-dev python3-dev: psycopg2 source dependencies
# * curl: to healthcheck services with http response
# * vim: editing files
# * procps: useful utilities such as ps, top, vmstat, pgrep,...
# Clean the apt cache
RUN apt-get update \
    && apt-get install -yq --no-install-recommends gcc libpq-dev python3-dev curl vim procps \
    && rm -rf /var/lib/apt/lists/*

# Add non-root user
RUN adduser --disabled-password --gecos "" $USERNAME

# Set working directory
WORKDIR ${PORTFOLIO_HOME}

# Copy dependencies files
ARG POETRY_LOCK_FILE=poetry.lock
ARG PYPROJECT_FILE=pyproject.toml
COPY $POETRY_LOCK_FILE $PYPROJECT_FILE ./

# Install poetry and app dependencies
ARG POETRY_VERSION=1.0.5
RUN pip install "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi \
    && rm $POETRY_LOCK_FILE $PYPROJECT_FILE

# Add project source code to /home/portfolio
ARG PORTFOLIO_TARBALL
ADD $PORTFOLIO_TARBALL /home/portfoliouser/

# Change ownership of /home/portfolio to portfoliouser
RUN chown -R ${USERNAME}:${USERNAME} ${PORTFOLIO_HOME}

# Set default user to be non-root portfoliouser
USER $USERNAME

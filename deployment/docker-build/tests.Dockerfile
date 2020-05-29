FROM python:3.8-slim-buster as base_build


ARG USERNAME="portfoliouser"
ENV PORTFOLIO_HOME="/home/${USERNAME}" \
    PYTHONPATH=${PORTFOLIO_HOME} \
    USERNAME=${USERNAME}

RUN apt-get update \
    && apt-get install -yq --no-install-recommends gcc libpq-dev python3-dev vim \
    && rm -rf /var/lib/apt/lists/* \
    && adduser --disabled-password --gecos "" $USERNAME

WORKDIR ${PORTFOLIO_HOME}

# Install Poetry and project dependencies
RUN pip install "poetry==1.0.5"
ARG POETRY_LOCK_FILE=poetry.lock
ARG PYPROJECT_FILE=pyproject.toml
COPY $POETRY_LOCK_FILE $PYPROJECT_FILE ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

RUN mkdir portfolio/ \
    && chown -R ${USERNAME}:${USERNAME} ${PORTFOLIO_HOME}

# USER $USERNAME
USER root
FROM python:3.8-slim-buster as base_build

ENV PYTHONPATH="/home/portfolio"

WORKDIR "/home/portfolio"

RUN apt-get update \
    && apt-get install -yq --no-install-recommends gcc libpq-dev python3-dev vim \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies files
COPY ./poetry.lock ./pyproject.toml ./

# Install Poetry and project dependencies
RUN pip install "poetry==1.0.5"
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi
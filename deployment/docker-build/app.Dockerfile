####################
#   BASE BUILD
####################

# pull official base image
FROM python:3.6.9-alpine as base_build

# Define labels
LABEL author="Guillaume Bournique <gbournique@gmail.com>"

ENV PORTFOLIO_HOME="/home/portfolio"
ENV APP_CODE="/home/portfolio/app"
ENV PYTHONPATH=${PORTFOLIO_HOME}

# Set work directory
WORKDIR ${PORTFOLIO_HOME}


####################
#   INSTALLER BUILD
####################
FROM base_build as installer_build

RUN apk update \
    # Install psycopg2 dependencies
    && apk add postgresql-dev gcc python3-dev musl-dev \
    # Install Pillow dependencies
    && apk add libpq jpeg-dev zlib-dev

# Install project dependencies
COPY deployment/docker-build/requirements.txt $PORTFOLIO_HOME/requirements.txt
RUN pip wheel --no-deps --wheel-dir $PORTFOLIO_HOME/wheels -r $PORTFOLIO_HOME/requirements.txt

# Install project dependencies with poetry
# RUN pip install poetry==1.0.5
# COPY ./poetry.lock ./pyproject.toml $PORTFOLIO_HOME
# RUN poetry install --no-dev --no-interaction --no-ansi

ARG PORTFOLIO_TARBALL
ADD $PORTFOLIO_TARBALL /home

ARG CELERY_STARTUP="deployment/docker-build/startup_celery.sh"
ARG SERVER_STARTUP="deployment/docker-build/startup_server.sh"
COPY $CELERY_STARTUP ${APP_CODE}/
COPY $SERVER_STARTUP ${APP_CODE}/
RUN chmod +x ${APP_CODE}/startup_celery.sh
RUN chmod +x ${APP_CODE}/startup_server.sh


####################
#   FINAL BUILD
####################
FROM base_build as final_build

# Copy project and dependencies built from previous stage build
COPY --from=installer_build $PORTFOLIO_HOME $PORTFOLIO_HOME
COPY --from=installer_build $PORTFOLIO_HOME/wheels /wheels

RUN pip install --upgrade pip \
    && pip install /wheels/* \
    # Install other dependencies
    && apk add curl \
    && apk add vim \
    # Install psycopg2 dependencies
    && apk add libpq jpeg-dev zlib-dev \
    # Clean up
    && rm -rf $PORTFOLIO_HOME/wheels \
    && rm $PORTFOLIO_HOME/requirements.txt

# Informs Docker that the container listens on 8000 at runtime
EXPOSE 8080

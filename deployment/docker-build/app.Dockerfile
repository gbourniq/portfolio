####################
#   BASE BUILD
####################

# pull official base image
FROM python:3.6.9-alpine as base_build

# Define labels
LABEL author="Guillaume Bournique <gbournique@gmail.com>"

ENV PYTHONPATH="/home/portfolio/"
ENV PORTFOLIO_HOME="/home"
ENV PORTFOLIO_CODE="/home/portfolio"
ENV APP_CODE="/home/portfolio/app"

# Set work directory
WORKDIR ${PORTFOLIO_HOME}



####################
#   INSTALLER BUILD
####################
FROM base_build as installer_build

# Install psycopg2 dependencies
RUN apk update \
    && apk add --no-cache postgresql-dev gcc python3-dev musl-dev
# Install Pillow dependencies
RUN apk add --no-cache libpq jpeg-dev zlib-dev
# Install other dependencies
RUN apk add --no-cache curl \
    && apk add --no-cache vim

# Install project dependencies
COPY deployment/docker-build/requirements.txt $PORTFOLIO_CODE/requirements.txt
RUN pip wheel --no-cache-dir --no-deps --wheel-dir $PORTFOLIO_CODE/wheels -r $PORTFOLIO_CODE/requirements.txt


# Install project dependencies with poetry
# RUN pip install poetry==1.0.5
# COPY ./poetry.lock ./pyproject.toml $PORTFOLIO_HOME
# RUN poetry install --no-dev --no-interaction --no-ansi

ARG PORTFOLIO_TARBALL

ADD $PORTFOLIO_TARBALL $PORTFOLIO_HOME

ARG CELERY_STARTUP="deployment/docker-build/startup_celery.sh"
ARG SERVER_STARTUP="deployment/docker-build/startup_server.sh"

COPY $CELERY_STARTUP ${APP_CODE}/startup_worker.sh
COPY $SERVER_STARTUP ${APP_CODE}/startup_server.sh

RUN chmod +x ${APP_CODE}/startup_worker.sh
RUN chmod +x ${APP_CODE}/startup_server.sh


####################
#   FINAL BUILD
####################
FROM base_build as final_build

# Copy project
# Copy $HOME directory and ignore the copy layer from installer_build
COPY --from=installer_build $PORTFOLIO_HOME $PORTFOLIO_HOME

# Copy dependencies built from previous stage build
COPY --from=installer_build $PORTFOLIO_CODE/wheels /wheels
RUN pip install --upgrade pip \
    && pip install --no-cache /wheels/* \
    && rm -rf $PORTFOLIO_CODE/wheels \
    && rm $PORTFOLIO_CODE/requirements.txt

WORKDIR ${PORTFOLIO_CODE}

# Informs Docker that the container listens on 8000 at runtime
EXPOSE 8080

###########
# BUILDER #
###########

# pull official base image
FROM python:3.8.0-alpine as builder

# Set work directory
RUN mkdir /code
WORKDIR /code

# Install psycopg2 dependencies
RUN apk update \
    && apk add --no-cache postgresql-dev gcc python3-dev musl-dev

# Install Pillow dependencies
RUN apk add --no-cache jpeg-dev zlib-dev \
    && apk add --no-cache --virtual .build-deps build-base linux-headers

# Install dependencies
COPY devops/docker-deployment/config/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /code/wheels -r requirements.txt


###########
#  FINAL  #
# ~175MB  #
###########

# Pull official base image
FROM python:3.8.0-alpine

# Define labels
ARG app_version
ARG app_component
LABEL application.version=${app_version}
LABEL application.component=${app_component}
LABEL author="Guillaume Bournique <gbournique@gmail.com>"

# Set environment variables
# Prevents Python from writing pyc files to disc
# Prevents Python from buffering stdout and stderr 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
ENV APP_HOME=/code
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Create directory for static and media files
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles

# Install dependencies
RUN apk update && apk add libpq --no-cache
COPY --from=builder /code/wheels /wheels
COPY --from=builder /code/requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache /wheels/*

# Copy entrypoint scripts
COPY devops/docker-deployment/config/run_server.sh $APP_HOME
COPY devops/docker-deployment/config/run_celery.sh $APP_HOME

# Copy project
COPY /app $APP_HOME

# Informs Docker that the container listens on 8000 at runtime
# EXPOSE 8080




##################
# DEV DOCKERFILE #
# IMAGE SIZE ~1GB
##################

# FROM python:3.7

# ARG app_version
# LABEL application.version=${app_version}
# LABEL application.component=backend
# LABEL author="Guillaume Bournique <gbournique@gmail.com>"

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # create the app user
# # RUN useradd -ms /bin/bash app_user
# # RUN adduser --disabled-password --gecos '' app_user

# # Set container working directory
# RUN mkdir /code
# WORKDIR /code

# # Install librairies
# COPY devops/docker-deployment/config/requirements.txt .
# RUN python -m pip install --upgrade pip \
#     && pip install -r requirements.txt

# # Copy entrypoint script
# COPY devops/docker-deployment/config/run_server.sh $APP_HOME
# COPY devops/docker-deployment/config/run_celery.sh $APP_HOME

# # Copy django app
# COPY /app .

# # Informs Docker that the container listens on 8000 at runtime
# EXPOSE 8080

# # chown all the files to the app user
# # RUN chown -R app_user /code

# # change to the app user
# # USER app_user
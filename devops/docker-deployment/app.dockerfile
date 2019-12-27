FROM python:3.7

ARG app_version
LABEL application.version=${app_version}
LABEL application.component=backend
LABEL author="Guillaume Bournique <gbournique@gmail.com>"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set container working directory
RUN mkdir /code
WORKDIR /code

# Install librairies
COPY devops/docker-deployment/config/requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy entrypoint script
COPY devops/docker-deployment/config/run_server.sh .

# Copy django app
COPY /app .

# Informs Docker that the container listens on 8000 at runtime
EXPOSE 8080

# Start django server
# defined in compose
# ENTRYPOINT [ "/bin/bash", "-c", "./run_server.sh" ]
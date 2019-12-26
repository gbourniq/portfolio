# docker image build -t myapp:latest -f ./Dockerfile.app ..

FROM node:latest

MAINTAINER Guillaume Bournique <gbournique@gmail.com>

ARG app_version
LABEL application.version=${app_version}
LABEL application.component=myapp-backend

# Set container working directory
WORKDIR /app

# Copy package dependencies file
COPY app/package.json /app/

# Install librairies
RUN npm install

# Copy whole project to 
COPY app/ /app/

# Informs Docker that the container listens on 4000 at runtime
EXPOSE ${APP_HTTP_PORT}

ENTRYPOINT ["/app/entrypoint.sh"]

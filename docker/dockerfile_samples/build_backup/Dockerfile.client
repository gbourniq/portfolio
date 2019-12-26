# docker image build -t myclient:latest -f ./Dockerfile.client ..

FROM node:latest

MAINTAINER Guillaume Bournique <gbournique@gmail.com>

ARG app_version
LABEL application.version=${app_version}
LABEL application.component=myapp-frontend

# Set working directory
WORKDIR /client

# Copy package dependencies file
COPY client/package.json /client/

# Install librairies
RUN npm install

# Copy whole project to 
COPY client/ /client/

# Informs Docker that the container listens on 3000 at runtime
EXPOSE ${CLIENT_HTTP_PORT}

ENTRYPOINT ["/client/entrypoint.sh"]


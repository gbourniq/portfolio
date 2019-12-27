FROM postgres:12-alpine

# shell script(docker entry point) specifying what commands to run on the database container, 
# things like creating the database, users and granting privileges to the said user.
WORKDIR /docker-entrypoint-initdb.d/
COPY devops/docker-deployment/config/run_db_setup.sh .

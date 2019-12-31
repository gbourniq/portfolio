FROM postgres:12-alpine

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=myportfoliodb
ENV POSTGRES_USER=postgres
ENV POSTGRES_SERVICE=postgres
ENV POSTGRES_PORT=5432
ENV LC_ALL=C.UTF-8

# shell script(docker entry point) specifying what commands to run on the database container, 
# things like creating the database, users and granting privileges to the said user.
WORKDIR /docker-entrypoint-initdb.d/
COPY deployment/build-images/config/run_db_setup.sh .

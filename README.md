### To-Do's
- write steps to build images
- write down steps to run it with docker-compose
- Portfolio - un-gitingore folders, and re-structure them one by one to work with app
    - docker folder
    - test githooks?
    - set up tests
    - travis steps
    - k8s
    



# Portfolio Application

This is the sample application for the Pluralsight course Docker in Production using AWS.

The application is based upon the excellent [Vert.x Microservices Workshop](https://github.com/cescoffier/vertx-microservices-workshop), although a number of modifications have been made as outlined below:

- Full continuous delivery workflow using Docker (based upon my course [Continuous Delivery using Docker and Ansible](https://www.pluralsight.com/courses/docker-ansible-continuous-delivery))
- Use of Gradle as the multi-project build tool.
- Use of the [Typesafe config library](https://github.com/typesafehub/config) for friendlier 12-factor environment variable based configuration support.
- Use of [Flyway](https://flywaydb.org) for lightweight database migrations
- Some of the individual microservices have been refactored to be more resilient to failure
- Addition of unit/integration tests and acceptance tests

## Contents

- [Application Architecture](#application-architecture)
- [Quick Start](#quick-start)
- [Docker Workflow](#docker-workflow)
- [Environment Configuration Settings](#environment-configuration-settings)
- [Branches](#branches)
- [Repository Timeline](#repository-timeline)
- [Errata](#errata)


## Application Architecture

The application consists of four Microservices that collectively comprise a simple fictitious stock trading application:

- [Quote Generator](./microtrader-quote) - periodically generates stock market quotes for three fictitious companies
- [Portfolio Service](./microtrader-portfolio) - trades stocks starting from an initial portfolio of $10000 cash on hand.  The trading logic is completely random and non-sensical.
- [Service discovery](http://vertx.io/docs/vertx-service-discovery/java/) - allows Microservices to discover, locate and interact with other services.  Vert.x includes a simple distributed map structure to store service discovery, however this can be replaced with several popular backends such as Consul and Kubernetes.


#### Scripts ####

These are scripts defined in `eigen_ui/package.json`.

|**Command**                   |**What it does**                                                    |
|------------------------------|-----------------                                                   |
|`npm run test`                | Runs the test suite                                                |
|`npm run test:watch`          | Runs the test suite in watch mode                                  |
|`npm run test:coverage`       | Runs tests and checks test coverage of code                        |
|`npm run test:teamcity-lint`  | Runs eslint outputting in teamcity format                          |
|`npm run test:lint`           | Run eslint                                                         |
|`npm run test:licenses`       | Collects all dependency licenses and appends them to package.json  |
|`npm run build`               | Produces a production build bundle                                 |
|`npm run start`               | Starts development server                                          |
|`npm run start-external`      | Starts development on external IP                                  |
|`npm run test:coverage-server`| Create coverage report and hosts it on 127.0.0.1:8080              |
|`npm run flow`                | Run static type checking on frontend                               |


## Quick Start

### Building the Application Locally

Before building and running the application locally, your system must have the following prerequisites installed:

- Java JDK 8
- NodeJS 4.x or higher (to install the `npm` package manager)
- Bower (`npm install -g bower`)

You first need to build "fat" jars for each Microservice, using the Gradle shadowJar plugin as shown below:

```
$ ./gradlew clean test shadowJar
...
...
:clean
```

### Application Versioning

The application uses a simple versioning scheme for all components:

  `<git-commit-timestamp>.<git-commit-short-hash>`

You can use the `make version` command to view the current version.  The versioning scheme also appends a build identifier if the `BUILD_ID` environment variable is set:

```
$ make version
20161018004318.d4ce05e

$ export BUILD_ID=1234
$ make version
20161018004318.d4ce05e.1234
```

### Running the Application Locally

To run the application locally, first execute audit database migrations as demonstrated below to create the initial DB schema. 

## Docker Workflow

The repository includes a Docker-based continuous delivery workflow that creates two environments:

- Test Environment
- Release Environment

### Test Environment

The test environment is expressed via a [`docker-compose.yml`](./docker/test/docker-compose.yml) file in the [docker/test](./docker/test) folder.

### Running the Workflow

To run the workflow your system must meet the following requirements:

- Docker 1.12 or higher client installed and pointed to a local or remote Docker Engine
- Docker Compose 1.7 or higher
- GNU Make

The workflow consists of the following tasks:

### Publishing Release Images

The final stage is to publish the release images.

To be able to publish your release images, you will need to reconfigure this project to point to a parent repository and Docker registry that you have write access to.

This can be achieved by editing the [`Makefile`](./Makefile) and configuring the `ORG_NAME` and `DOCKER_REGISTRY` settings:

```
...
...
# Project variables
```

### Cleaning Up

To clean up the Docker environments, run the `make clean` task:

```
$ make clean
=> Destroying test environment...
...
```

### Running an End-to-end Workflow

The workflow includes a convenient `make all` task, which automatically runs the following tasks:

- `make clean`
- `make test`
- `make release`
- `make tag:default` - tags the current version (i.e. `make version`), short commit hash, any annotated tags that are present on the current commit and the 'latest' tag
- `make publish`
- `make clean` 


### Running an End-to-end Workflow

Write about:
- Pre-commit / black
- Ansible stuff
- Travis CLI stuff
- bump2version
- makefile commands
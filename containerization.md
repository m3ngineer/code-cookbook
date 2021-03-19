# Containerization of Code

Containers are isolated environments and processes that help to keep code running consistently between development and production.

Docker is one of the most commonly used containers, defined as

> A container is a standard unit of software that packages up code and all its dependencies so the application runs quickly and reliably from one computing environment to another.

Docker consists of a Dockerfile and Docker Compose.

## Dockerfile

Dockerfiles are text documents that contain all the commands a user would call to assemble an image.

```Dockerfile
FROM python:3.8-alpine3.11

# update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.11/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.11/community" >> /etc/apk/repositories

# install chromedriver
RUN apk --no-cache add chromium chromium-chromedriver

# install selenium
RUN pip install selenium pytest
```

To build your image:

```Shell
docker build . -t <image-name>:<tag>
```

To run your image:

```Shell
docker run -it <image-name>:<tag> sh
```

To view information about active containers:

```Shell
docker ps
docker run -it <image-name>:<tag> sh
```

## Docker Compose
A Dockerfile will contain the core image used to construct the container base. However, your application will likely require other dependencies, environment variables, and specific settings to run.

[Docker Compose](https://docs.docker.com/compose/) is used to standardize the assembly of more complex containers specific for an application. Docker Compose files are YAML files with configurations used to start the app's services. Docker Compose consists of:

1) A Dockerfile containing the application's environment setup
2) A docker-compose.yml that defines the services that make up the app
3) Running `docker compose up` to start the app

An example docker-compose.yml file:

#### docker-compose.yml

```YAML
version: '3'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/code
    environment:
      FLASK_ENV: development
      REDIS_HOST: redis
      REDIS_PORT: 6379
  redis:
    image: "redis:alpine"
```

There are several pieces in the configuration file to break down:
- **services:** this is the parent tag that contains all of the containers
- **build:** the base image to use
- **ports:** the ports to expose in the format host port: container port
- **volumes:** In Docker, containers are composed of read-only layers. If a file is modified, it is saved in a read-write layer that sits on top of the read layer. This combination of read-only and read-write layers are called the Union File System. The read layers are preserved, but hidden by the read-write layer, and the read-write layer is lost once the container is dissolved. Volumes are directories (or files) that are outside of the default Union File System and exist as normal directories and files on the host filesystem. These are Docker's way of persisting data and sharing data between containers. Volumes can be specified as a new path to be created by the Engine (var/path/opt), a path map between the host and container volume (host/path:container/path), or a named path (volumename:var/path/opt)
- **comands:** set of commands to run upon container start
- **environment:** environment variables; these can be assigned in the file, persist from the shell, or be passed through a .env file

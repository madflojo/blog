---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Don't mock Databases, just run them with Docker"
subtitle: "How to use Docker Compose to make unit testing easier"
summary: "Use Docker Compose to create on-demand databases within your local & build environments"
authors: ["Benjamin Cane"]
tags: ["docker", "golang", "continuous integration", "ci/cd"]
categories: ["Software Engineering"]
date: 2020-06-15T00:20:53-07:00
lastmod: 2020-06-15T00:20:53-07:00
featured: true
draft: false
url: /2020/06/15/dont-mock-a-db-use-docker-compose
aliases: ["/post/dont-mock-a-db-use-docker-compose/"]

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: false

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects: []
---

I see this one question pop up in channels over and over again. 

> "What is the best way to mock a database for unit tests?"

For most, the thought of mocking responses from a database is daunting. Taking each DB call and creating a unique mock response can be a lot of work, especially within a large service.

This article proposes an alternative idea. One that I've been using for both open source and enterprise applications. 

Rather than spending forever creating mocks of a database. Run the database itself as part of your continuous integration (CI) pipeline. With todays tools, this is easy, but it hasn't always been this way.

## Running Databases for Unit testing used to suck

In the past, setting up a database to use with unit testing was a hassle. It meant running a database service on either a physical or virtual server. Once you get a server, the following install process is generally long itself.

In big companies, this could mean working with many teams, which elongates the process. This alone is a common deterrent for using a real database within unit tests.

Even after going through the process, it is often cost or time prohibitive to get more than one sever. This makes it even more difficult to use within a CI pipeline.

Most applications have many developers. Trying to use a single database service for every developer doesn't work. It's very difficult to coordinate more than one build at a time. 

With the speed of development these days, running a pipeline one build at a time is a major hinderance. It's also a waste of time.

What I've seen people do in response is only run the tests on the `main` branch build. Where pull requests or local unit test runs don't run these tests. This means less testing is performed on pull requests and more testing is done after merge. This in itself is fundamentally flawed.

The point of executing builds on pull requests is to ensure that new changes work with existing code. Once merged everything should just work. If pull requests are lacking in tests, than there is a higher likelihood of breaking the `main` build.

Which means rolling back changes, this is difficult on high velocity repositories. With many pull requests being submitted and merged in the same day. It can be very difficult finding which change broke the build.

## Modern CI tools give you a better option

Today's continuous integration tools give us a better option. Rather than running a dedicated database outside of the build environment. Use Docker to run a database instance within the build environment.

Modern CI tools such as [CircleCI](https://circleci.com/) have this feature so baked in, it's fundamental to using the service. In this article, we will discuss a way to run isolated Database instances anywhere. From your local system to even the most basic build environments. As long as you can execute `docker` and `docker-compose` commands. This article will work.

## Better builds with Docker Compose

For this article I'm going to use one of my side projects as an example. That project is [Hord](https://github.com/madflojo/hord). Hord is a Go package that aims to provide a consistent Key-Value interface for any database.

Hord is a good example for this article for a few reason. The first being that since it is a package, functional testing doesn't really apply well. All the testing performed on a Hord build is unit testing.

Another reason is that the package supports multiple databases. With a goal of supporting many more. For this type of package, trying to mock each database is an arduous task.

> **Note:** In this article we will only setup a Cassandra cluster, but the concept can be repeated for any other database.

### Pre-Requisite: Install Docker and Docker Compose

While this article is all about using Docker and Docker Compose in the CI pipeline. Unit tests should always be executable locally. As such we will need to install both Docker and Docker Compose on our local machine.

This article is going to show installing Docker and Docker Compose on Ubuntu Bionic which is the latest LTS release with full Docker support. For other OS options you can reference the following guides.

*   [Docker Install Guide](https://docs.docker.com/engine/install/)
*   [Docker Compose Install Guide](https://docs.docker.com/compose/install/)

We will start the installation by installing our dependencies first.

```console
$ sudo su -
# apt-get install -y apt-transport-https ca-certificates curl gnupg-agent python-pip
```

Next we will add the Docker Apt repository to our local repository list. Once added we will also need to update our local repository indexes.

```console
# curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add 
# add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
# apt-get update
```

Once Apt is ready, we can install the Docker Engine with `apt-get`.

```console
# apt-get install -y docker-ce docker-ce-cli containerd.io
```

With Docker Engine installed, we can now install Docker Compose. While there are many ways to install it, I find the easiest is to use the `pip` Python package installer.

```console
# pip install docker-compose
```

With the above complete we can now able to run Docker and Docker Compose.

### Creating a Compose file

Originally, Compose started as a tool to allow users to define container manifests. It gives users a way to specify how to start a service. As well as any dependent containers and options they need.

Let's take a look at a simple Compose example.

```yaml
version: "3"
services:
  mockitout:
    build: .
    ports:
      - "443:8443"
    command: --debug 
    environment:
      - "LISTEN_ADDR=0.0.0.0:8443"
```

The above example looks simple but it does a lot. It starts a service named `mockitout`. It builds the container image using the `.` (current working directory) path. It maps the host port `443` to the internal container port `8443`. It passes an environment variable `LISTEN_ADDR` to the container. And finally, it overrides the default command with `--debug`.

If we were to launch this service manually, it would be two commands. One of them being a very long `docker run` command with a lot of arguments. With Compose, we can start this service by executing a `docker-compose up`.

When you consider that most compose files consist of many services. You can start to understand how much time and effort Docker Compose saves us.

#### Using Compose for CI

For our purpose, we will be using Docker Compose to run CI steps and services. This is very different than the traditional role Compose has played. The most common usage for Docker Compose is to start a service. In our Compose file, we are going to do everything but that.

As such, when using Compose for CI, I tend to use a non-default name and call it `dev-compose.yml`. I've had several instances where someone new to the project, will see a `docker-compose.yml` file (the default). And without looking at the contents of the file run a `docker-compose up`.

To avoid confusion, I reserve `docker-compose.yml` for the base service manifest. I then use `dev-compose.yml` for any development related Compose definitions.

Our first step to using Compose for CI, is going to be to create the `dev-compose.yml` file.

```console
$ vi dev-compose.yml
```

For our example project, we have quite a few services to setup. The first, will be a service called `tests`. This will be a service that actually runs our Go unit tests. These tests will fail of course, because we need to spin up our dependencies. For which we will be running a Cassandra cluster.

#### Defining the tests service

Technically, we don't need to have our unit tests run inside of a Docker container. We could still do all that we need using Docker Compose to launch just the databases.

I however, like to run my unit tests inside of a container. I do this for a few reasons.

First, by running my unit tests inside of a docker container my build is portable. I can move my project from one CI platform to another. I do not have to worry if the build environment has the right version of Go.

The Second, is essentially the same, except it applies to developer machines. Every developer has a different setup, different Go version, different IDE, different whatever. By requiring developers to run tests via Compose. I am ensuring that when they run local, it's the same as running in the CI environment. Now, this does take some getting used to. Often times developers hate leaving their IDE, even if it is for a shell prompt.

Once folks get used to working this way however, they are often much more efficient. As using Compose to run dependencies locally, is often freeing. It allows developers to focus not on how to connect to or setup a dependency, but rather on developing.

The one negative I've seen with this approach however, is that it can sometimes add time to the build. If managed well, not much time, but if managed poorly, it can add lots of time.

The reason for this is because when you run the unit tests you also need to build the Docker image it runs within. This might mean installing any dependencies like GCC, or even packages. Go has fast build times, so this doesn't tend to be a problem for me. But for some other languages, where dependencies are pulled every build. This can add up.

With that said, let's define our `tests` container.

```yaml
version: "3"
services:
  tests:
    build: .
    working_dir: /go/src/github.com/madflojo/hord
    command: go test -v ./...
```


In the above example we can see familiar parameters from before like `build` and `command`. The `command` parameter is important for this container as this is the command we wish to launch with. This `go test` command will execute all the unit tests within that directory and its children.

#### Defining the Cassandra services

With our `tests` container created we now need to setup the Cassandra cluster that our tests are going to use. We will do this by adding the following services.

```yaml
  cassandra-primary:
    image: madflojo/cassandra:latest
    command: /bin/bash -c "sleep 1 && /docker-entrypoint.sh cassandra -f"
    environment:
      - CASSANDRA_KEYSPACE=hord
    expose:
      - 7000
      - 7001
      - 7199
      - 9042
      - 9160
  cassandra:
    image: madflojo/cassandra:latest
    command: /bin/bash -c "sleep 15 && /docker-entrypoint.sh cassandra -f"
    environment:
      - CASSANDRA_SEEDS=cassandra-primary
      - CASSANDRA_KEYSPACE=hord
    depends_on:
      - cassandra-primary
    expose:
      - 7000
      - 7001
      - 7199
      - 9042
      - 9160
```

In this example we have two services defined, `cassandra-primary` and `cassandra`. We have Cassandra broken up into two services due to the way Cassandra clustering works. We need to start a single instance first allowing that instance to be our primary instance. Our second instance is going to boot and pair up with the primary instance.

Once both instances are booted, our cluster will be ready to be tested against. If we want to launch this cluster we can run the following Docker Compose command.

```console
$ docker-compose -f dev-compose.yml up cassandra-primary cassandra
```

#### Linking our services

While it's great to be able to launch our Cassandra cluster locally with one simple command. What we really want to do, is have our cluster automatically start whenever our tests are run. To do this we need to tell Compose that our `tests` service depends on the `cassandra` and `cassandra-primary` services. We can accomplish this by editing our `tests` service and adding the `depends_on` configuration.

```yaml
  tests:
    build: .
    depends_on:
      - cassandra
      - cassandra-primary
    working_dir: /go/src/github.com/madflojo/hord
    entrypoint: go test -v ./...
```

Once these are added, we can start both our `tests` and Cassandra cluster with one command.

```console
$ docker-compose -f dev-compose.yml up --build tests
```

### Adding Compose to our Build

Now that we can run our Go tests local, we need to integrate them into our CI builds. For this step I'm going to leverage [Travis CI](https://travis-ci.com/) which is a popular CI service. I'm using this service because of the way Travis CI works. 

Travis CI works by creating a `.travis.yml` file. Within this file you can run any shell command you want to perform your build. If we can get our Docker Compose process to work here, we can pretty much get it to work anywhere. 

To get started we will put the following in our `.travis.yml` file at the top level of our repository.

```yaml
language: go
go:
  - 1.14.1
os:
  - linux
env:
  - "PATH=/home/travis/gopath/bin:$PATH"
before_script:
  - go mod tidy
script:
  - docker-compose -f dev-compose.yml up -d cassandra-primary cassandra
  - sleep 30
  - docker-compose -f dev-compose.yml up --exit-code-from tests --build tests
```

Now let's breakdown this file a bit. The `language`, `go`, and `os` definitions are used to tell Travis which base build environment we need. With the settings we have, we will be building using a `Linux` image with Go 1.14.1 installed.

The `before_script` definition are tasks we want to execute before our build "script". The `script` definition is where the build actually happens. In this build step we are first starting the Cassandra cluster, then our `tests` service. This is to avoid any timing issues with the Go tests trying to execute before the cluster is ready. 

The command to start the `tests` service should look familiar, as we used it earlier. However, there is a new option being given. The `--exit-code-from` flag tells Compose to use the exit code from a specific container as the return code for the `docker-compose` command.

We want our build to fail if our tests fails. But we are using Compose to launch many containers. By telling Compose to use the exit code of the `tests` container, we can ensure our build fails if our tests fail.

With the above `.travis.yml` file. We can now run through our build process. To trigger this simply push these files to your connected repository.

## Summary

In this article we discussed how to avoid mocking databases by using Docker to run them. We showed how today's tools make it easier to do this. We did this using some very basic tools, but these are not the only tools available to us. For users of [GitHub](https://github.com) or [GitLab](https://gitlab.com) this can all be accomplished using their CI/Actions services. Most modern CI systems also allow you to run Docker containers.

The point isn't the tools you use, it's how they are used. What you want, is for developers to be able to run the same steps as a pipeline locally. You want everything you need to test against available within your build environment. One very simple way to get there, is to use Docker Compose.

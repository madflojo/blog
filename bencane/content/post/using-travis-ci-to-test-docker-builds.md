---
authors:
- Benjamin Cane
categories:
- Docker
- Containers
- Continuous Integration
date: '2016-01-11T14:00:00'
description: Walk-through on getting started with Travis CI and how to use Travis
  CI to test Docker builds
draft: false
header:
  caption: ''
  image: ''
tags:
- docker
- dockerfile
- dockerizing
- containers
- linux containers
- linux docker
- docker blog
- application packaging
- nginx docker
- linux
- travis ci
- travis
- integration
- automated testing
title: Using Travis CI to test Docker builds
url: /2016/01/11/using-travis-ci-to-test-docker-builds

---
In last months article we discussed ["Dockerizing" this blog](http://bencane.com/2015/12/01/getting-started-with-docker-by-dockerizing-this-blog/). What I left out from that article was how I also used Docker Hub's [automatic builds](https://docs.docker.com/docker-hub/builds/) functionality to automatically create a new image every time changes are made to the GitHub Repository which contains the source for this blog.

The automatic builds are useful because I can simply make changes to the code or articles within the repository and once pushed, those changes trigger Docker Hub to build an image using the `Dockerfile` we created in the previous article. As an extra benefit the Docker image will also be available via Docker Hub, which means any system with Docker installed can deploy the latest version by simply executing `docker run -d madflojo/blog`. 

The only gotcha is; what happens if those changes break things? What if a change prevents the build from occurring, or worse prevents the static site generator from correctly generating pages. What I need is a way to know if changes are going to cause issues or not before they are merged to the `master` branch of the repository; deploying those changes to production.

To do this, we can utilize **Continuous Integration** principles and tools.

## What is Continuous Integration

Continuous Integration or CI, is something that has existed in the software development world for a while but it has gained more following in the operations world recently. The idea of CI came up to address the problem of multiple developers creating integration problems within the same code base. Basically, two developers working on the same code creating conflicts and not finding those conflicts until much later.

The basic rule goes, the later you find issues within code the more expensive (time and money) it is to fix those issues. The idea to solve this is for developers to commit their code into source control often, multiple times a day even. With code commits being pushed frequently this reduces the opportunity for code integration problems, and when they do happen it is often a lot easier to fix.

However, code commits multiple times a day by itself doesn't solve integration issues. There also needs to be a way to ensure the code being committed is quality code and works. This brings us to another concept of CI, where every time code is committed, the code is built and tested automatically.

In the case of this blog, the build would consist of building a Docker image, and testing would consist of some various tests I've written to ensure the code that powers this blog is working appropriately. To perform these automated builds and test executions we need a tool that can detect when changes happen, and perform the necessary steps; we need a tool like [Travis CI](https://travis-ci.org).

## Travis CI

[Travis CI](https://travis-ci.org/) is a Continuous Integration tool that integrates with GitHub and performs automated build and test actions. It is also free for public GitHub repositories, like this blog for instance.

In this article I am going to walk through configuring Travis CI to automatically build and test the Docker image being generated for this blog. Which, will give you (the reader) the basics of how to use Travis CI to test your own Docker builds.

## Automating a Docker build with Travis CI

This post is going to assume that we have already signed up for Travis CI and connected it to our public repository. This process is fairly straight forward, as it is part of Travis CI's on-boarding flow. If you find yourself needing a good walk through, Travis CI does have a [getting started](https://docs.travis-ci.com/user/getting-started/#To-get-started-with-Travis-CI%3A) guide.

Since we will be testing our builds and do not wish to impact the main `master` branch the first thing we are going to do is create a new `git` branch to work with.

    $ git checkout -b building-docker-with-travis
 
As we make changes to this branch we can push the contents to GitHub under the same branch name and validate the status of Travis CI builds without those changes going into the `master` branch.

### Configuring Travis CI

Within our new branch we will create a `.travis.yml` file. This file essentially contains configuration and instructions for Travis CI. Within this file we will be able to tell Travis CI what languages and services we need for the build environment as well as the instructions for performing the build.

### Defining the build environment

Before starting any build steps we first need to define what the build environment should look like. For example, since the `hamerkop` application and associated testing scripts are written in Python, we will need Python installed within this build environment.

While we could install Python with a few `apt-get` commands, since Python is the only language we need within this environment it's better to define it as the base language using the `language: python` parameter within the `.travis.yml` file.

    language: python
    python:
      - 2.7
      - 3.5

The above configuration informs Travis CI to set the build environment to a Python environment; specifically for Python versions **2.7** and **3.5** to be installed and supported.

The syntax used above is in YAML format, which is a fairly popular configuration format. In the above we are essentially defining the `language` parameter as **python** and setting the `python` parameter to a list of versions **2.7** and **3.5**. If we wanted to add additional versions it is as simple as appending that version to this list; such as in the example below.

    language: python
    python:
      - 2.7
      - 3.2
      - 3.5

In the above we simply added version **3.2** by adding it to the list.


#### Required services

As we will be building a Docker image we will also need Docker installed and the Docker service running within our build environment. We can accomplish this by using the `services` parameter to tell Travis CI to install Docker and start the service.

    services:
      - docker

Like the `python` parameter the `services` parameter is a list of services to be started within our environment. As such that means we can also include additional services by appending to the list. If we needed Docker and Redis for example we can simply append the line after specifying the Docker service.

    services:
      - docker
      - redis-server

In this example we do not require any service other than Docker, however it is useful to know that Travis CI has quite a few [services available](https://docs.travis-ci.com/user/database-setup/).

### Performing the build

Now that we have defined the build environment we want, we can execute the build steps. Since we wish to validate a Docker build we essentially need to perform two steps, building a Docker container image and starting a container based on that image. 

We can perform these steps by simply specifying the same `docker` commands we used in the previous article.

    install:
      - docker build -t blog .
      - docker run -d -p 127.0.0.1:80:80 --name blog blog

In the above we can see that the two `docker` commands are specified under the `install` parameter. This parameter is actually a defined build step for Travis CI.

Travis CI has multiple predefined steps used during builds which can be called out via the `.travis.yml` file. In the above we are defining that these two `docker` commands are the steps necessary to install this application.

### Testing the build

Travis CI is not just a simple build tool, it is a Continuous Integration tool which means its primary function is testing. Which means we need to add a test to our build; for now we can simply verify that the Docker container is in running, which can be performed by a simple `docker ps` command.

    script:
      - docker ps | grep -q blog

In the above we defined our basic test using the `script` parameter. This is yet another build step which is used to call test cases. The `script` step is a required step, if omitted the build will fail.

#### Pushing to GitHub

With the steps above defined we now have a minimal build that we can send to Travis CI; to accomplish this, we simply push our changes to GitHub.

    $ git add .travis.yml 
    $ git commit -m "Adding docker build steps to Travis"
    [building-docker-with-travis 2ad7a43] Adding docker build steps to Travis
     1 file changed, 10 insertions(+), 32 deletions(-)
     rewrite .travis.yml (72%)
    $ git push origin building-docker-with-travis

During the sign up process for Travis CI, you are asked to link your repositories with Travis CI. This allows it to monitor the repository for any changes. When changes occur, Travis CI will automatically pull down those changes and execute the steps defined within the `.travis.yml` file. Which in this case, means executing our Docker build and verifying it worked.

As we just pushed new changes to our repository, Travis CI should have detected those changes. We can go to [Travis CI](https://travis-ci.org/madflojo/blog) to verify whether those changes resulted in a successful build or not.

Travis CI, will show a build log for every build, at the end of the log for this specific build we can see that the build was successful.

    Removing intermediate container c991de57cced
    Successfully built 45e8fb68a440
    $ docker run -d -p 127.0.0.1:80:80 --name blog blog
    45fe9081a7af138da991bb9e52852feec414b8e33ba2007968853da9803b1d96
    $ docker ps | grep -q blog
    
    The command "docker ps | grep -q blog" exited with 0.
    
    Done. Your build exited with 0.

One important thing to know about Travis CI is that most build steps require commands to execute successfully in order for the build to be marked as successful. 

The `script` and `install` steps are two examples of this, if any of our commands failed and did not return a `0` [exit code](http://bencane.com/2014/09/02/understanding-exit-codes-and-how-to-use-them-in-bash-scripts/) than the whole build would be marked as failed.

If this happens during the `install` step, the build will be stopped at the exact step that failed. With the `script` step however, the build will not be stopped. The idea behind this is that if an install step fails, the build will absolutely not work. However, if a single test case fails only a portion is broken. By showing all testing results users will be able to identify what is broken vs. what is working as expected.

## Adding additional tests

While we now have Travis CI able to verify the Docker build is successful, there are still other ways we could inadvertently break this blog. For example, we could make a change that prevents the static site generator from properly generating pages, this would break the site within the container but not necessarily the container itself. To prevent a scenario like this, we can introduce some additional testing.

Within our repository there is a directory called `tests`, this directory contains three more directories; `unit`, `integration` and `functional`. These directories contain various automated tests for this environment. The first two types of tests `unit` and `integration` are designed to specifically test the code within the `hamerkop.py` application. While useful, these tests are not going to help test the Docker container. However, the last directory `functional`, contains automated tests that can be used to test the running Docker container.

    $ ls -la tests/functional/
    total 24
    drwxr-xr-x 1 vagrant vagrant  272 Jan  1 03:22 .
    drwxr-xr-x 1 vagrant vagrant  170 Dec 31 22:11 ..
    -rw-r--r-- 1 vagrant vagrant 2236 Jan  1 03:02 test_broken_links.py
    -rw-r--r-- 1 vagrant vagrant 2155 Jan  1 03:22 test_content.py
    -rw-r--r-- 1 vagrant vagrant 1072 Jan  1 03:13 test_rss.py

These tests are designed to connect to the running Docker container and validate the static site's content.

For example `test_broken_links.py` will crawl the website being served by the Docker container and check the HTTP status code returned when requesting each page. If the return code is anything but `200 OK` the test will fail. The `test_content.py` test will also crawl the site and validate the content returned matches a certain pattern. If it does not, then again these tests will fail.

What is useful about these tests is that, even though the static site is running within a Docker container we are still able to test the site functionality. If we were to add these tests to the Travis CI configuration, they would also be executed for every code change; providing even more confidence about each change being made.

### Installing test requirements in `before_script`

To run these tests via Travis CI we will simply need to add them to the `script` section as we did with the `docker ps` command. However, before they can be executed these tests require several Python libraries to be installed. To install these libraries we can add the installation steps into the `before_script` build step.

    before_script:
      - pip install -r requirements.txt
      - pip install mock
      - pip install requests
      - pip install feedparser

The `before_script` build step is performed before the `script` step but after the `install` step. Making `before_script` the perfect location for steps that are required for `script` commands but not part of the overall installation. Since the `before_script` step is not executing test cases like the `install` step, it too requires all commands to succeed before moving to the `script` build step. If a command within the `before_script` build step fails, the build will be stopped.

### Running additional tests

With the required Python libraries installed we can add the test execution to the `script` build step.

    script:
      - docker ps | grep -q blog
      - python tests.py

These tests can be launched by executing `tests.py`, which will run all 3 automated tests; `unit`, `integration` and `functional`.

### Testing the build again

With the tests added we can once again push our changes to GitHub.

    $ git add .travis.yml
    $ git commit -m "Adding tests.py execution"
    [building-docker-with-travis 99c4587] Adding tests.py execution
     1 file changed, 14 insertions(+)
    $ git push origin building-docker-with-travis

After pushing our updates to the repository we can sit back and wait for Travis to build and test our application.

    ######################################################################
    Test Runner: Functional tests
    ######################################################################
    runTest (test_rss.VerifyRSS)
    Execute recursive request ... ok
    runTest (test_broken_links.CrawlSite)
    Execute recursive request ... ok
    runTest (test_content.CrawlSite)
    Execute recursive request ... ok
    
    ----------------------------------------------------------------------
    Ran 3 tests in 0.768s
    
    OK

Once the build completes we will see the above message in the build log, showing that Travis CI has in fact executed our tests.

## Summary

With our builds successfully processing let's take a final look at our `.travis.yml` file.

```
language: python
python:
  - 2.7

services:
  - docker

install:
  - docker build -t blog .
  - docker run -d -p 127.0.0.1:80:80 --name blog blog

before_script:
  - pip install -r requirements.txt
  - pip install mock
  - pip install requests
  - pip install feedparser

script:
  - docker ps | grep -q blog
  - python tests.py
```

In the above we can see our Travis CI configuration consists of 3 build steps; `install`, `before_script` and `script`. The `install` step is used to build and start our Docker container. The `before_script` step is simply used to install required libraries for test scripts and the `script` step is used to execute our test scripts.

Overall, this setup is pretty simple and something we could test manually outside of Travis CI. The benefit of having Travis CI though is that all of these steps are performed for every change, no matter how minor they are.

Also since we are using GitHub, this means Travis CI will append build status notifications on every pull request as well, like [this one for example](https://github.com/madflojo/blog/pull/18). With these types of notifications I can merge pull requests into the `master` branch with the confidence that they will not break production.

### Building a Continuous Integration and Deployment pipeline

In last months article we explored [using Docker to package and distribute](http://bencane.com/2015/12/01/getting-started-with-docker-by-dockerizing-this-blog/) the application running this blog. In this article, we have discussed leveraging Travis CI to automatically build that Docker image as well as performing functional tests against it.

In next months article, we are going to take this setup one step further by automatically deploying these changes to multiple servers using SaltStack. By the end of the next article we will have a full Continuous Integration and Deployment work-flow defined which will allow changes to be tested and deployed to production without human interaction.

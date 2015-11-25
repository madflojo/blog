Docker is an interesting technology that over the past 2 years has gone from an idea, to being used by organizations all over the world to rapidly deploy applications. In today's article I am going to cover how to get started with Docker by "Dockerizing" an existing application. The application in question is actually this very blog!

## What is Docker

Before we dive into learning the basics of Docker let's first understand what Docker is and why it is so popular. Docker, is a operating system container management system that allows you to easily manage and deploy applications that are bundled within operating system containers.

### Containers vs. Virtual Machines

Containers may not be as familiar as virtual machines but they are another method to provide **Operating System Virtualization**. However, they differ quite a bit from standard virtual machines.

Standard virtual machines generally include a full Operating System, OS Packages and eventually an Application or two. This is made possible by a Hypervisor which provides hardware virtualization to the virtual machine. This allows for a single server to run many stand alone operating systems as virtual guests.

Containers are similar to virtual machines in that they allow a single server to run multiple operating environments, these environments however, are not full operating systems. Containers generally only include the necessary OS Packages and Applications. They do not contain a full operating system or hardware virtualization. This also means that containers have a smaller overhead than traditional virtual machines.

Containers and Virtual Machines are often seen as conflicting technology, however, this is often a misunderstanding. Virtual Machines are a way to take a physical server and provide a fully functional operating environment that shares those physical resources with other virtual machines. A Container is generally used to isolate a running process within a single host to ensure that the isolated processes cannot interact with other processes within that same system. In fact **Containers** are closer to **BSD Jails** and `chroot`ed processes than full virtual machines.

### What Docker provides on top of containers

Docker itself is not a container runtime environment; it is actually a tool that is container technology agnostic with efforts planned for Docker to support [Solaris Zones](https://blog.docker.com/2015/08/docker-oracle-solaris-zones/) and [BSD Jails](https://wiki.freebsd.org/Docker). What Docker provides is a method of managing, packaging, and deploying containers. While these types of functions may exist to some degree for virtual machines they traditionally have not existed for most container solutions and the ones that did exist, did not match the functionality that Docker provides.

Now that we know what Docker is, let's start learning how Docker works by first installing Docker and deploying a pre-built container.

## Starting with Installation

As Docker is not installed by default on Linux we will need to install the Docker package; since our example system is running Ubuntu 14.0.4 we will do this by executing the `apt-get` command.

    # apt-get install docker.io
    Reading package lists... Done
    Building dependency tree       
    Reading state information... Done
    The following extra packages will be installed:
      aufs-tools cgroup-lite git git-man liberror-perl
    Suggested packages:
      btrfs-tools debootstrap lxc rinse git-daemon-run git-daemon-sysvinit git-doc
      git-el git-email git-gui gitk gitweb git-arch git-bzr git-cvs git-mediawiki
      git-svn
    The following NEW packages will be installed:
      aufs-tools cgroup-lite docker.io git git-man liberror-perl
    0 upgraded, 6 newly installed, 0 to remove and 0 not upgraded.
    Need to get 7,553 kB of archives.
    After this operation, 46.6 MB of additional disk space will be used.
    Do you want to continue? [Y/n] y

Once installed we can see if any containers are running by executing `docker ps`.

    # docker ps
    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES

The `ps` function of the `docker` command works similar to the Linux `ps` command. It will show available Docker containers and their current status. Since we have not started any Docker containers yet the command shows no running containers.

## Deploy a pre-built nginx Docker container

One of my favorite features of Docker is the ability to deploy a pre-built container in the same way you would deploy a package with `yum` or `apt-get`. To explain this better let's deploy a pre-built container running the **nginx** webserver by executing `docker run nginx`.

    # docker run nginx
    Unable to find image 'nginx' locally
    Pulling repository nginx
    5c82215b03d1: Download complete 
    e2a4fb18da48: Download complete 
    58016a5acc80: Download complete 
    657abfa43d82: Download complete 
    dcb2fe003d16: Download complete 
    c79a417d7c6f: Download complete 
    abb90243122c: Download complete 
    d6137c9e2964: Download complete 
    85e566ddc7ef: Download complete 
    69f100eb42b5: Download complete 
    cd720b803060: Download complete 
    7cc81e9a118a: Download complete 

In another shell we can see this new container running by executing `docker ps`.

    # docker ps
    CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS              PORTS               NAMES
    f6d31ab01fc9        nginx:latest        nginx -g 'daemon off   4 seconds ago       Up 3 seconds        443/tcp, 80/tcp     desperate_lalande 

We can now see a container named `desperate_lalande` running and that this container is an image of `nginx:latest`. 

### Docker Images

Docker images are one of it's key features. Like a virtual machine image, a Docker image is a container that has been saved and packaged. Along with the ability to create images, Docker also includes the ability to distribute those images via Docker repositories. This is what gives Docker the ability to deploy an image like you would deploy a package with `yum`. To get a better understanding of how this works let's look back at the output of the `docker run nginx` execution.

    # docker run nginx
    Unable to find image 'nginx' locally

The first message we see is that `docker` could not find an image named **nginx** locally. The reason we see this message is because when we executed `docker run` we told Docker to startup a container, a container based on an image named **nginx**. The first task Docker will perform is to check if there is a local image with the specified name. Since this system is brand new there was no Docker images with the name **nginx** on this system, which means in order to deploy a container using the **nginx** image it will need to download it from a Docker repository.

    Pulling repository nginx
    5c82215b03d1: Download complete 
    e2a4fb18da48: Download complete 
    58016a5acc80: Download complete 
    657abfa43d82: Download complete 
    dcb2fe003d16: Download complete 
    c79a417d7c6f: Download complete 
    abb90243122c: Download complete 
    d6137c9e2964: Download complete 
    85e566ddc7ef: Download complete 
    69f100eb42b5: Download complete 
    cd720b803060: Download complete 
    7cc81e9a118a: Download complete 

Which is exactly what the second part of this output is showing us. By default `docker` uses the [Docker Hub](https://hub.docker.com/) repository, which is a repository service that Docker (the company) runs. Like GitHub, Docker Hub is free for public repositories and paid for private repositories. It is possible to deploy your own Docker repository, in fact it is as easy as `docker run registry`.

For this article we will not be deploying a custom registry; we will save that for another article.

At this point

## Building our own image

Now that we have explored how to deploy a pre-built container, we can move to "Dockerizing" this blog. What that means is we are going to create a custom container that deploys this blog.

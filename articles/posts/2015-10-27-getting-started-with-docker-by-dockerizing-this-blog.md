Docker is an interesting technology that over the past 2 years has gone from an idea, to being used by organizations all over the world to rapidly deploy applications. In today's article I am going to cover how to get started with Docker by "Dockerizing" an existing application. The application in question is actually this very blog!

## What is Docker

Before we dive into learning the basics of Docker let's first understand what Docker is and why it is so popular. Docker, is a operating system container management system that allows you to easily manage and deploy applications by allowing you to package them within operating system containers.

### Containers vs. Virtual Machines

Containers may not be as familiar as virtual machines but they are another method to provide **Operating System Virtualization**. However, they differ quite a bit from standard virtual machines.

Standard virtual machines generally include a full Operating System, OS Packages and eventually an Application or two. This is made possible by a Hypervisor which provides hardware virtualization to the virtual machine. This allows for a single server to run many stand alone operating systems as virtual guests.

Containers are similar to virtual machines in that they allow a single server to run multiple operating environments, these environments however, are not full operating systems. Containers generally only include the necessary OS Packages and Applications. They do not contain a full operating system or hardware virtualization. This also means that containers have a smaller overhead than traditional virtual machines.

Containers and Virtual Machines are often seen as conflicting technology, however, this is often a misunderstanding. Virtual Machines are a way to take a physical server and provide a fully functional operating environment that shares those physical resources with other virtual machines. A Container is generally used to isolate a running process within a single host to ensure that the isolated processes cannot interact with other processes within that same system. In fact **Containers** are closer to **BSD Jails** and `chroot`ed processes than full virtual machines.

### What Docker provides on top of containers

Docker itself is not a container runtime environment; it is actually a tool that is container technology agnostic with efforts planned for Docker to support [Solaris Zones](https://blog.docker.com/2015/08/docker-oracle-solaris-zones/) and [BSD Jails](https://wiki.freebsd.org/Docker). What Docker provides is a method of managing, packaging, and deploying containers. While these types of functions may exist to some degree for virtual machines they traditionally have not existed for most container solutions and the ones that did exist, were not as easy to use or fully featured as Docker.

Now that we know what Docker is, let's start learning how Docker works by first installing Docker and deploying a pre-built container.

## Starting with Installation

As Docker is not installed by default we will need to first install the Docker package before starting a container. Since our example system is running Ubuntu 14.0.4 we will do this using the **Apt** package manager.

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

The `ps` function of the `docker` command works similar to the Linux `ps` command. It will show available Docker containers and their current status. Since we have not started any Docker containers yet, the command shows no running containers.

## Deploy a pre-built nginx Docker container

One of my favorite features of Docker is the ability to deploy a pre-built container in the same way you would deploy a package with `yum` or `apt-get`. To explain this better let's deploy a pre-built container running the **nginx** webserver by simply executing `docker run nginx`.

    # docker run -d nginx
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

From the output we can now see a container named `desperate_lalande` running and that this container is an image of `nginx:latest`. 

### Docker Images

Images is one of Docker's key features. Like a virtual machine image, a Docker image is a container that has been saved and packaged. Docker however, doesn't just stop with the ability to create images. Docker also includes the ability to distribute those images via Docker repositories which are a similar concept to **Git** or Package repositories. This is what gives Docker the ability to deploy an image like you would deploy a package with `yum`. To get a better understanding of how this works let's look back at the output of the `docker run` execution.

    # docker run -d nginx
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

Which is exactly what the second part of this output is showing us. By default `docker` uses the [Docker Hub](https://hub.docker.com/) repository, which is a repository service that Docker (the company) runs. Like GitHub, Docker Hub is free for public repositories and paid for private repositories. It is possible however, to deploy your own Docker repository, in fact it is as easy as `docker run registry`. For this article we will not be deploying a custom registry.

### Stopping and Removing the Container

So far we have learned how to start a Docker container, in order to stop a running container we simply need to execute the `docker kill` command and specify the container name.

    # docker kill desperate_lalande
    desperate_lalande

If we run the `docker ps` command again we will see that the container is no longer running.

    # docker ps
    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES

However, at this point we have only stopped the container. The container still exists but is simply not running. We can see the status of containers that are running or not running by adding the `-a` flag to the `docker ps` command.

    # docker ps -a
    CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS                           PORTS               NAMES
    f6d31ab01fc9        5c82215b03d1        nginx -g 'daemon off   4 weeks ago         Exited (-1) About a minute ago                       desperate_lalande  

In order to fully remove the container we can execute the `docker rm` command.

    # docker rm desperate_lalande
    desperate_lalande

Now that this container has been removed we no longer have a **nginx** container, but we still have the **nginx** image available. If we were to re-run the `docker run` command again we would not need to fetch the **nginx** image as it is already saved to our local system. To see a list of all available images we can simply run the `docker images` command.

    # docker images
    REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
    nginx               latest              9fab4090484a        5 days ago          132.8 MB

## Building our own image

At this point we have used a few basic Docker commands to start, stop and remove a pre-built public image. In order to "Dockerize" this blog however, we are going to need to do more than start a container. In order to turn this blog into a Docker container we are going to have to build our own Docker image.

### The Dockerfile

With most virtual machine environments if you wish to create an image you need to create a new virtual machine, install the OS, install the application and convert it to a template or image. With Docker however, these steps are actually automated via a Dockerfile. A Dockerfile is a way of providing build instructions to Docker for the creation of a custom image. In this section we are going to build a custom Dockerfile from scratch that deploys this blog.

#### Understanding the Application

Before we can jump into the Dockerfile we first need to understand what is required to deploy this blog. The blog itself is actually static html pages generated by a Static Site Generator that I wrote and recently updated. The generator is very simple and custom to this blog. This blog is hosted as a public [GitHub](https://github.com/madflojo/blog) repository which contains the code for the Static Site Generator, HTML Templates, Images and the Articles. For us to deploy this blog we simply need to clone the **GitHub** repository and execute the Static Site Generator. The underlying web server that I use for my blog is **nginx**; which means we will need to build a Docker image that grabs the latest code/articles, installs and then runs nginx.

So far this should be a pretty simple Dockerfile, but it will show us quite a bit of the [Dockerfile Syntax](https://docs.docker.com/v1.8/reference/builder/). Let's get started by cloning the **GitHub** repository and creating a Dockerfile with our favorite editor; `vi` in my case.

    # git clone https://github.com/madflojo/blog.git
    Cloning into 'blog'...
    remote: Counting objects: 622, done.
    remote: Total 622 (delta 0), reused 0 (delta 0), pack-reused 622
    Receiving objects: 100% (622/622), 14.80 MiB | 1.06 MiB/s, done.
    Resolving deltas: 100% (242/242), done.
    Checking connectivity... done.
    # cd blog/
    # vi Dockerfile

#### FROM

The first instruction of a Dockerfile is the `FROM` instruction. This is used to specify an existing Docker image to use as our base image. This basically provides us with a starting point to work from. If we wanted to start with the latest stable **Ubuntu** Docker image we can simply specify `FROM ubuntu:latest`. For our case we will save ourselves the hassle of installing **nginx** by using the **nginx** Docker image as our base.

    ## Dockerfile that generates an instance of http://bencane.com
    
    FROM nginx:latest
    MAINTAINER Benjamin Cane <ben@bencane.com>

In the above I also included the `MAINTAINER` instruction which is used to show the Author of the Dockerfile and not necessarily a critical component. You may also notice from the above that there is a comment at the top of the Dockerfile. Docker supports using the `#` as a comment marker allowing you to document a Dockerfile like you would a shell script.

#### Running a test build

Since we inherited the **nginx** Docker image our current Dockerfile also inherited all of the instructions built into the [Dockerfile](https://github.com/nginxinc/docker-nginx/blob/08eeb0e3f0a5ee40cbc2bc01f0004c2aa5b78c15/Dockerfile) used to build that **nginx** image. What this means is even at this point we are able to build a Docker image from this Dockerfile and run a container from that image. This image will essentially be the same as the **nginx** image at this point but we will run through a build of this Dockerfile to show how that our Dockerfile is correct and results in a working container.

In order to build a Docker image from a Dockerfile we can simply execute the `docker build` command and specify the directory that contains the Dockerfile.

    # docker build -t blog /root/blog 
    Sending build context to Docker daemon  23.6 MB
    Sending build context to Docker daemon 
    Step 0 : FROM nginx:latest
     ---> 9fab4090484a
    Step 1 : MAINTAINER Benjamin Cane <ben@bencane.com>
     ---> Running in c97f36450343
     ---> 60a44f78d194
    Removing intermediate container c97f36450343
    Successfully built 60a44f78d194

In the above example I used the `-t` flag with the `docker build` command to "tag" the image. This essentially allows us to name the image, without specifying a tag the image would only be callable via a `IMAGE ID` value that Docker assigns. In this case the image id is `60a44f78d194` which we can see being referenced in the output above.

Now that we have an image that starts and deploys an **nginx** webserver let's start making this custom image deploy the blog.

#### RUN and ADD

Since the static site generator used to create this blog is written in **python** there are a few tasks we need to execute before we can execute the generator. The first thing we should do is to create a directory that will contain all of the necessary code, images and article files required to build the blog. To have Docker execute a command during an image build we can use the `RUN` instruction.

    ## Dockerfile that generates an instance of http://bencane.com
    
    FROM nginx:latest
    MAINTAINER Benjamin Cane <ben@bencane.com>
    
    ## Create a directory for required files
    RUN mkdir -p /build/

In the above we have added the `RUN` instruction for Docker to execute while building this image. One important thing to understand about the `RUN` instruction is that this command is only run within the container being built. This means that the `/root/blog/` directory that contains the Dockerfile will remain untouched.

Since we now have a build directory let's also install some required OS packages, we can do this again via the `RUN` instruction calling the `apt-get` command.

    ## Dockerfile that generates an instance of http://bencane.com
    
    FROM nginx:latest
    MAINTAINER Benjamin Cane <ben@bencane.com>
    
    ## Create a directory for required files
    RUN mkdir -p /build/
    ## Install python and pip
    RUN apt-get update
    RUN apt-get install -y python-dev python-pip

In the above we can see that we first needed to run `apt-get update` to refresh **Apt** package managers cache of available repositories and then finally executed `apt-get install` to install the required python packages. It is also important to call out that the `apt-get install` command was executed with the `-y` flag which has the effect of accepting any prompts `apt-get` has along the way. One fact to keep in mind is that Docker image builds do not accept user input during the build process. What this means is that any command being execute must complete without any user input outside of the Dockerfile.

If we build the **blog** image again, we can see something very interesting.

    # docker build -t blog /root/blog/
    Sending build context to Docker daemon  23.6 MB
    Sending build context to Docker daemon 
    Step 0 : FROM nginx:latest
     ---> 9fab4090484a
    Step 1 : MAINTAINER Benjamin Cane <ben@bencane.com>
     ---> Using cache
     ---> 8e0f1899d1eb
    Step 2 : RUN mkdir -p /build/
     ---> Using cache
     ---> 3601f3bfbf53
    Step 3 : RUN apt-get update
     ---> Running in 804e07ee3389
    Get:1 http://security.debian.org jessie/updates InRelease [63.1 kB]
    Ign http://nginx.org jessie InRelease
    <truncated to reduce noise>
    Get:10 http://httpredir.debian.org jessie/main amd64 Packages [9035 kB]
    Fetched 9581 kB in 43s (219 kB/s)
    Reading package lists...
     ---> 9e11c3d60b63
    Removing intermediate container 804e07ee3389
    Step 4 : RUN apt-get install -y python-dev python-pip
     ---> Running in f42c617a8750
    Reading package lists...
    Building dependency tree...
    Reading state information...
    The following extra packages will be installed:
      binutils build-essential bzip2 cpp cpp-4.9 dpkg-dev fakeroot file g++
    <truncated to reduce noise>
    Setting up python-pip (1.5.6-5) ...
    update-alternatives: using /usr/bin/file-rename to provide /usr/bin/rename (rename) in auto mode
    Processing triggers for libc-bin (2.19-18+deb8u1) ...
    Processing triggers for python-support (1.0.15) ...
     ---> 4c5ab00d983c
    Removing intermediate container f42c617a8750
    Successfully built 4c5ab00d983c

In the above we can see that steps that were executed in previous builds of this image have the following message `---> Using cache`. What this is telling us is that Docker was able to use it's build cache to speed up the build of this image.

##### Docker Build Cache

When Docker is building an image, it doesn't just build a single image it actually builds multiple images along the way. In fact we can see that in the above output after each "Step"; `---> 8e0f1899d1eb`. We can see from the output above that after "Step 1" Docker generated an image named `8e0f1899d1eb`. During subsequent builds of this same image, Docker is able to reuse those images as a cache.

If we go back to our Dockerfile we now have both **nginx** and **python** installed, however the site generator requires a few python packages. To install these we will use the `pip` command.

    ## Dockerfile that generates an instance of http://bencane.com
    
    FROM nginx:latest
    MAINTAINER Benjamin Cane <ben@bencane.com>
    
    ## Create a directory for required files
    RUN mkdir -p /build/
    ## Install python and pip
    RUN apt-get update
    RUN apt-get install -y python-dev python-pip
    
    ## Add requirements file and run pip
    ADD requirements.txt /build/requirements.txt
    RUN pip install -r /build/requirements.txt

Within the **Git** repository for this blog there is a file called `requirements.txt` which lists all of the python libraries required for the static site generator. A simple way of installing these required libraries with `pip` is to simply run it by specify `install -r`. The `-r` flag is used to specify a "requirements" file for `pip` to read and install the specified libraries. You may notice however, before executing the `pip` command we used a new Dockerfile instruction `ADD`. The `ADD` instruction provides the ability add a file that exists within the same directory as the Dockerfile to the Docker image.

In the Dockerfile above we have added the `requirements.txt` file to the `/build/` directory. If we did not add this file with the `ADD` instruction our `pip` command would fail as that file would simply not exist.



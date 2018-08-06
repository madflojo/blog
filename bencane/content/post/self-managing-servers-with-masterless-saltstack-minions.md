---
authors:
- Benjamin Cane
categories:
- Continuous Delivery
- SaltStack
- Docker
date: '2016-03-22T14:30:00'
description: Using Saltstack's Masterless Minion architecture to create self-managing
  infrastructure
draft: false
header:
  caption: ''
  image: ''
tags:
- docker
- dockerfile
- dockerizing
- docker blog
- linux
- continuous delivery
- salt
- saltstack
- masterless saltstack
- minionless saltstack
- salt-ssh
- salt over ssh
- deployment automation
title: Create self-managing servers with Masterless Saltstack Minions
url: /2016/03/22/self-managing-servers-with-masterless-saltstack-minions

---

Over the past two articles I've described building a Continuous Delivery pipeline for my blog (the one you are currently reading). The first article covered [packaging the blog into a Docker container](http://bencane.com/2015/12/01/getting-started-with-docker-by-dockerizing-this-blog/) and the second covered [using Travis CI to build the Docker image and perform automated testing against it](http://bencane.com/2016/01/11/using-travis-ci-to-test-docker-builds/).

While the first two articles covered quite a bit of the CD pipeline there is one piece missing; automating deployment. While there are many infrastructure and application tools for automated deployments I've chosen to use Saltstack. I've chosen Saltstack for many reasons but the main reason is that it can be used to manage both my host system's configuration and the Docker container for my blog application. Before I can start using Saltstack however, I first need to set it up.

I've covered [setting up Saltstack](http://bencane.com/2013/09/03/getting-started-with-saltstack-by-example-automatically-installing-nginx/) before, but for this article I am planning on setting up Saltstack in a Masterless architecture. A setup that is quite different from the traditional Saltstack configuration.

## Masterless Saltstack

A traditional Saltstack architecture is based on a Master and Minion design. With this architecture the Salt Master will push desired states to the Salt Minion. This means that in order for a Salt Minion to apply the desired states it needs to be able to connect to the master, download the desired states and then apply them.

A masterless configuration on the other hand involves only the Salt Minion. With a masterless architecture the Salt state files are stored locally on the Minion bypassing the need to connect and download states from a Master. This architecture provides a few benefits over the traditional Master/Minion architecture. The first is removing the need to have a Salt Master server; which will help reduce infrastructure costs, an important item as the environment in question is dedicated to hosting a simple personal blog.

The second benefit is that in a masterless configuration each Salt Minion is independent which makes it very easy to provision new Minions and scale out. The ability to scale out is useful for a blog, as there are times when an article is reposted and traffic suddenly increases. By making my servers self-managing I am able to meet that demand very quickly.

A third benefit is that Masterless Minions have no reliance on a Master server. In a traditional architecture if the Master server is down for any reason the Minions are unable to fetch and apply the Salt states. With a Masterless architecture, the availability of a Master server is not even a question.

## Setting up a Masterless Minion

In this article I will walk through how to install and configure a Salt in a masterless configuration.

### Installing `salt-minion`

The first step to creating a Masterless Minion is to install the `salt-minion` package. To do this we will follow the official steps for Ubuntu systems outlined at [docs.saltstack.com](https://docs.saltstack.com/en/latest/topics/installation/ubuntu.html). Which primarily uses the Apt package manager to perform the installation.

#### Importing Saltstack's GPG Key

Before installing the `salt-minion` package we will first need to import Saltstack's Apt repository key. We can do this with a simple `bash` one-liner.

```
# wget -O - https://repo.saltstack.com/apt/ubuntu/14.04/amd64/latest/SALTSTACK-GPG-KEY.pub | sudo apt-key add -
OK
```

This GPG key will allow Apt to validate packages downloaded from Saltstack's Apt repository.

#### Adding Saltstack's Apt Repository

With the key imported we can now add Saltstack's Apt repository to our `/etc/apt/sources.list` file. This file is used by Apt to determine which repositories to check for available packages.

    # vi /etc/apt/sources.list

Once editing the file simply append the following line to the bottom.

    deb http://repo.saltstack.com/apt/ubuntu/14.04/amd64/latest trusty main

With the repository defined we can now update Apt's repository inventory. A step that is required before we can start installing packages from the new repository.

#### Updating Apt's cache

To update Apt's repository inventory, we will execute the command `apt-get update`.

```
# apt-get update
Ign http://archive.ubuntu.com trusty InRelease                                 
Get:1 http://security.ubuntu.com trusty-security InRelease [65.9 kB]           
Get:2 http://archive.ubuntu.com trusty-updates InRelease [65.9 kB]             
Get:3 http://repo.saltstack.com trusty InRelease [2,813 B]                     
Get:4 http://repo.saltstack.com trusty/main amd64 Packages [8,046 B]           
Get:5 http://security.ubuntu.com trusty-security/main Sources [105 kB]         
Hit http://archive.ubuntu.com trusty Release.gpg                              
Ign http://repo.saltstack.com trusty/main Translation-en_US                    
Ign http://repo.saltstack.com trusty/main Translation-en                       
Hit http://archive.ubuntu.com trusty Release                                   
Hit http://archive.ubuntu.com trusty/main Sources                              
Hit http://archive.ubuntu.com trusty/universe Sources                          
Hit http://archive.ubuntu.com trusty/main amd64 Packages                       
Hit http://archive.ubuntu.com trusty/universe amd64 Packages                   
Hit http://archive.ubuntu.com trusty/main Translation-en                       
Hit http://archive.ubuntu.com trusty/universe Translation-en                   
Ign http://archive.ubuntu.com trusty/main Translation-en_US                    
Ign http://archive.ubuntu.com trusty/universe Translation-en_US                
Fetched 3,136 kB in 8s (358 kB/s)                                              
Reading package lists... Done
```

With the above complete we can now access the packages available within Saltstack's repository.

#### Installing with `apt-get`

Specifically we can now install the `salt-minion` package, to do this we will execute the command `apt-get install salt-minion`.

```
# apt-get install salt-minion
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following extra packages will be installed:
  dctrl-tools libmysqlclient18 libpgm-5.1-0 libzmq3 mysql-common
  python-dateutil python-jinja2 python-mako python-markupsafe python-msgpack
  python-mysqldb python-tornado python-zmq salt-common
Suggested packages:
  debtags python-jinja2-doc python-beaker python-mako-doc
  python-egenix-mxdatetime mysql-server-5.1 mysql-server python-mysqldb-dbg
  python-augeas
The following NEW packages will be installed:
  dctrl-tools libmysqlclient18 libpgm-5.1-0 libzmq3 mysql-common
  python-dateutil python-jinja2 python-mako python-markupsafe python-msgpack
  python-mysqldb python-tornado python-zmq salt-common salt-minion
0 upgraded, 15 newly installed, 0 to remove and 155 not upgraded.
Need to get 4,959 kB of archives.
After this operation, 24.1 MB of additional disk space will be used.
Do you want to continue? [Y/n] y
Get:1 http://archive.ubuntu.com/ubuntu/ trusty-updates/main mysql-common all 5.5.47-0ubuntu0.14.04.1 [13.5 kB]
Get:2 http://repo.saltstack.com/apt/ubuntu/14.04/amd64/latest/ trusty/main python-tornado amd64 4.2.1-1 [274 kB]
Get:3 http://archive.ubuntu.com/ubuntu/ trusty-updates/main libmysqlclient18 amd64 5.5.47-0ubuntu0.14.04.1 [597 kB]
Get:4 http://repo.saltstack.com/apt/ubuntu/14.04/amd64/latest/ trusty/main salt-common all 2015.8.7+ds-1 [3,108 kB]
Processing triggers for libc-bin (2.19-0ubuntu6.6) ...
Processing triggers for ureadahead (0.100.0-16) ...
```

After a successful installation of the `salt-minion` package we now have a `salt-minion` instance running with the default configuration.

### Configuring the Minion

With a Traditional Master/Minion setup, this point would be where we configure the Minion to connect to the Master server and restart the running service.

For this setup however, we will be skipping the Master server definition. Instead we will need to tell the `salt-minion` service to look for Salt state files locally. To alter the `salt-minion`'s configuration we can either edit the `/etc/salt/minion` configuration file which is the default configuration file. Or we could add a new file into `/etc/salt/minion.d/`; this `.d` directory is used to override default configurations defined in `/etc/salt/minion`.

My personal preference is to create a new file within the `minion.d/` directory, as this keeps the configuration easy to manage. However, there is no right or wrong method; as this is a personal and environmental preference.

For this article we will go ahead and create the following file `/etc/salt/minion.d/masterless.conf`.

    # vi /etc/salt/minion.d/masterless.conf

Within this file we will add two configurations.

```
file_client: local
file_roots:
  base:
    - /srv/salt/base
  bencane:
    - /srv/salt/bencane
```

The first configuration item above is `file_client`. By setting this configuration to `local` we are telling the `salt-minion` service to search locally for desired state configurations rather than connecting to a Master.

The second configuration is the `file_roots` dictionary. This defines the location of Salt state files. In the above example we are defining both `/srv/salt/base` and `/srv/salt/bencane`. These two directories will be where we store our Salt state files for this Minion to apply.

### Stopping the `salt-minion` service

While in most cases we would need to restart the `salt-minion` service to apply the configuration changes, in this case, we actually need to do the opposite; we need to stop the `salt-minion` service.

```
# service salt-minion stop
salt-minion stop/waiting
```

The `salt-minion` service does not need to be running when setup as a Masterless Minion. This is because the `salt-minion` service is only running to listen for events from the Master. Since we have no master there is no reason to keep this service running. If left running the `salt-minion` service will repeatedly try to connect to the defined Master server which by default is a host that resolves to `salt`. To remove unnecessary overhead it is best to simply stop this service in a Masterless Minion configuration.

### Populating the desired states

At this point we have a Salt Minion that has been configured to run masterless. However, at this point the Masterless Minion has no Salt states to apply. In this section we will provide the `salt-minion` agent two sets of Salt states to apply. The first will be placed into the `/srv/salt/base` directory. This `file_roots` directory will contain a base set of Salt states that I have created to manage a basic Docker host.

#### Deploying the base Salt states

The states in question are available via a public [GitHub repository](https://github.com/madflojo/salt-base). To deploy these Salt states we can simply clone the repository into the `/srv/salt/base` directory. Before doing so however, we will need to first create the `/srv/salt` directory.

```
# mkdir -p /srv/salt
```

The `/srv/salt` directory is Salt's default state directory, it is also the parent directory for both the `base` and `bencane` directories we defined within the `file_roots` configuration. Now that the parent directory exists, we will clone the `base` repository into this directory using `git`.

```
# cd /srv/salt/
# git clone https://github.com/madflojo/salt-base.git base
Cloning into 'base'...
remote: Counting objects: 50, done.
remote: Total 50 (delta 0), reused 0 (delta 0), pack-reused 50
Unpacking objects: 100% (50/50), done.
Checking connectivity... done.
```

As the `salt-base` repository is copied into the `base` directory the Salt states within that repository are now available to the `salt-minion` agent.

```
# ls -la /srv/salt/base/
total 84
drwxr-xr-x 18 root root 4096 Feb 28 21:00 .
drwxr-xr-x  3 root root 4096 Feb 28 21:00 ..
drwxr-xr-x  2 root root 4096 Feb 28 21:00 dockerio
drwxr-xr-x  2 root root 4096 Feb 28 21:00 fail2ban
drwxr-xr-x  2 root root 4096 Feb 28 21:00 git
drwxr-xr-x  8 root root 4096 Feb 28 21:00 .git
drwxr-xr-x  3 root root 4096 Feb 28 21:00 groups
drwxr-xr-x  2 root root 4096 Feb 28 21:00 iotop
drwxr-xr-x  2 root root 4096 Feb 28 21:00 iptables
-rw-r--r--  1 root root 1081 Feb 28 21:00 LICENSE
drwxr-xr-x  2 root root 4096 Feb 28 21:00 ntpd
drwxr-xr-x  2 root root 4096 Feb 28 21:00 python-pip
-rw-r--r--  1 root root  106 Feb 28 21:00 README.md
drwxr-xr-x  2 root root 4096 Feb 28 21:00 screen
drwxr-xr-x  2 root root 4096 Feb 28 21:00 ssh
drwxr-xr-x  2 root root 4096 Feb 28 21:00 swap
drwxr-xr-x  2 root root 4096 Feb 28 21:00 sysdig
drwxr-xr-x  3 root root 4096 Feb 28 21:00 sysstat
drwxr-xr-x  2 root root 4096 Feb 28 21:00 timezone
-rw-r--r--  1 root root  208 Feb 28 21:00 top.sls
drwxr-xr-x  2 root root 4096 Feb 28 21:00 wget
```

From the above directory listing we can see that the `base` directory has quite a few Salt states. These states are very useful for managing a basic Ubuntu system as they perform steps such as installing Docker (`dockerio`), to setting the system timezone (`timezone`). Everything needed to run a basic Docker host is available and defined within these base states.

#### Applying the base Salt states

Even though the `salt-minion` agent can now use these Salt states, there is nothing running to tell the `salt-minion` agent it should do so. Therefore the desired states are not being applied.

To apply our new base states we can use the `salt-call` command to tell the `salt-minion` agent to read the Salt states and apply the desired states within them.

    # salt-call --local state.highstate

The `salt-call` command is used to interact with the `salt-minion` agent from command line. In the above the `salt-call` command was executed with the `state.highstate` option.

This tells the agent to look for all defined states and apply them. The `salt-call` command also included the `--local` option, this option is specifically used when running a Masterless Minion. This flag tells the `salt-minion` agent to look through it's local state files rather than attempting to pull from a Salt Master.

The below shows the results of the execution above, within this output we can see the various states being applied successfully.

```
----------
          ID: GMT
    Function: timezone.system
      Result: True
     Comment: Set timezone GMT
     Started: 21:09:31.515117
    Duration: 126.465 ms
     Changes:   
              ----------
              timezone:
                  GMT
----------
          ID: wget
    Function: pkg.latest
      Result: True
     Comment: Package wget is already up-to-date
     Started: 21:09:31.657403
    Duration: 29.133 ms
     Changes:   

Summary for local
-------------
Succeeded: 26 (changed=17)
Failed:     0
-------------
Total states run:     26
```

In the above output we can see that all of the defined states were executed successfully. We can validate this further if we check the status of the `docker` service. Which we can see from below is now running; where before executing `salt-call`, Docker was not installed on this system.

```
# service docker status
docker start/running, process 11994
```

With a successful `salt-call` execution our Salt Minion is now officially a Masterless Minion. However, even though our server has Salt installed, and is configured as a Masterless Minion, there are still a few steps we need to take to make this Minion **"Self Managing"**.

## Self-Managing Minions

In order for our Minion to be Self-Managed, the Minion server should not only apply the base states above, it should also keep the `salt-minion` service and configuration up to date as well. To do this, we will be cloning yet another `git` repository.

### Deploying the blog specific Salt states

This repository however, has specific Salt states used to manage the `salt-minion` agent, for not only this but also any other Masterless Minion used to host this blog.

```
# cd /srv/salt
# git clone https://github.com/madflojo/blog-salt bencane
Cloning into 'bencane'...
remote: Counting objects: 25, done.
remote: Compressing objects: 100% (16/16), done.
remote: Total 25 (delta 4), reused 20 (delta 2), pack-reused 0
Unpacking objects: 100% (25/25), done.
Checking connectivity... done.
```

In the above command we cloned the [blog-salt](https://github.com/madflojo/blog-salt) repository into the `/srv/salt/bencane` directory. Like the `/srv/salt/base` directory the `/srv/salt/bencane` directory is also defined within the `file_roots` that we setup earlier.

### Applying the blog specific Salt states

With these new states copied to the `/srv/salt/bencane` directory, we can once again run the `salt-call` command to trigger the `salt-minion` agent to apply these states.

```
# salt-call --local state.highstate
[INFO    ] Loading fresh modules for state activity
[INFO    ] Fetching file from saltenv 'base', ** skipped ** latest already in cache u'salt://top.sls'
[INFO    ] Fetching file from saltenv 'bencane', ** skipped ** latest already in cache u'salt://top.sls'
----------
          ID: /etc/salt/minion.d/masterless.conf
    Function: file.managed
      Result: True
     Comment: File /etc/salt/minion.d/masterless.conf is in the correct state
     Started: 21:39:00.800568
    Duration: 4.814 ms
     Changes:   
----------
          ID: /etc/cron.d/salt-standalone
    Function: file.managed
      Result: True
     Comment: File /etc/cron.d/salt-standalone updated
     Started: 21:39:00.806065
    Duration: 7.584 ms
     Changes:   
              ----------
              diff:
                  New file
              mode:
                  0644

Summary for local
-------------
Succeeded: 37 (changed=7)
Failed:     0
-------------
Total states run:     37
```

Based on the output of the `salt-call` execution we can see that `7` Salt states were executed successfully. This means that the new Salt states within the `bencane` directory were applied. But what exactly did these states do?

### Understanding the "Self-Managing" Salt states

This second repository has a hand full of states that perform various tasks specific to this environment. The "Self-Managing" states are all located within the `srv/salt/bencane/salt` directory.

```
$ ls -la /srv/salt/bencane/salt/
total 20
drwxr-xr-x 5 root root 4096 Mar 20 05:28 .
drwxr-xr-x 5 root root 4096 Mar 20 05:28 ..
drwxr-xr-x 3 root root 4096 Mar 20 05:28 config
drwxr-xr-x 2 root root 4096 Mar 20 05:28 minion
drwxr-xr-x 2 root root 4096 Mar 20 05:28 states
```

Within the `salt` directory there are several more directories that have defined Salt states. To get started let's look at the `minion` directory. Specifically, let's take a look at the `salt/minion/init.sls` file.

```
# cat salt/minion/init.sls
salt-minion:
  pkgrepo:
    - managed
    - humanname: SaltStack Repo
    - name: deb http://repo.saltstack.com/apt/ubuntu/14.04/amd64/latest {{ grains['lsb_distrib_codename'] }} main
    - dist: {{ grains['lsb_distrib_codename'] }}
    - key_url: https://repo.saltstack.com/apt/ubuntu/14.04/amd64/latest/SALTSTACK-GPG-KEY.pub
  pkg:
    - latest
  service:
    - dead
    - enable: False

/etc/salt/minion.d/masterless.conf:
  file.managed:
    - source: salt://salt/config/etc/salt/minion.d/masterless.conf

/etc/cron.d/salt-standalone:
  file.managed:
    - source: salt://salt/config/etc/cron.d/salt-standalone
```

Within the `minion/init.sls` file there are 5 Salt states defined.

#### Breaking down the `minion/init.sls` states

Let's break down some of these states to better understand what actions they are performing.

```
  pkgrepo:
    - managed
    - humanname: SaltStack Repo
    - name: deb http://repo.saltstack.com/apt/ubuntu/14.04/amd64/latest {{ grains['lsb_distrib_codename'] }} main
    - dist: {{ grains['lsb_distrib_codename'] }}
    - key_url: https://repo.saltstack.com/apt/ubuntu/14.04/amd64/latest/SALTSTACK-GPG-KEY.pub
```

The first state defined is a `pkgrepo` state. We can see based on the options that this state is use to manage the Apt repository that we defined earlier. We can also see from the `key_url` option, that even the **GPG** key we imported earlier is managed by this state.

```
  pkg:
    - latest
```

The second state defined is a `pkg` state. This is used to manage a specific package, specifically in this case the `salt-minion` package. Since the `latest` option is present the `salt-minion` agent will not only install the latest `salt-minion` package but also keep it up to date with the latest version if it is already installed.

```
  service:
    - dead
    - enable: False
```

The third state is a `service` state. This state is used to manage the `salt-minion` service. With the `dead` and `enable: False` settings specified the `salt-minion` agent will stop and disable the `salt-minion` service.

So far these states are performing the same steps we performed manually above. Let's keep breaking down the `minion/init.sls` file to understand what other steps we have told Salt to perform.

```
/etc/salt/minion.d/masterless.conf:
  file.managed:
    - source: salt://salt/config/etc/salt/minion.d/masterless.conf
```

The fourth state is a `file` state, this state is deploying a `/etc/salt/minion.d/masterless.conf` file. This just happens to be the same file we created earlier. Let's take a quick look at the file being deployed to understand what Salt is doing.

```
$ cat salt/config/etc/salt/minion.d/masterless.conf
file_client: local
file_roots:
  base:
    - /srv/salt/base
  bencane:
    - /srv/salt/bencane
```

The contents of this file are exactly the same as the `masterless.conf` file we created in the earlier steps. This means that while right now the configuration file being deployed is the same as what is currently deployed. In the future if any changes are made to the `masterless.conf` within this `git` repository, those changes will then be deployed on the next `state.highstate` execution.

```
/etc/cron.d/salt-standalone:
  file.managed:
    - source: salt://salt/config/etc/cron.d/salt-standalone
```

The fifth state is also a `file` state, while this state is also deploying a file the file in question is very different. Let's take a look at this file to understand what it is used for.

```
$ cat salt/config/etc/cron.d/salt-standalone
*/2 * * * * root su -c "/usr/bin/salt-call state.highstate --local 2>&1 > /dev/null"
```

The `salt-standalone` file is a `/etc/cron.d` based cron job that appears to be running the same `salt-call` command we ran earlier to apply the local Salt states. In a masterless configuration there is no scheduled task to tell the `salt-minion` agent to apply all of the Salt states. The above cron job takes care of this by simply executing a local `state.highstate` execution every 2 minutes.

##### Summary of `minion/init.sls`

Based on the contents of the `minion/init.sls` we can see how this `salt-minion` agent is configured to be **"Self-Managing"**. From the above we were able to see that the `salt-minion` agent is configured to perform the following steps.

1. Configure the Saltstack Apt repository and GPG keys
2. Install the `salt-minion` package or update to the newest version if already installed
3. Deploy the `masterless.conf` configuration file into `/etc/salt/minion.d/`
4. Deploy the `/etc/cron.d/salt-standalone` file which deploys a cron job to initiate `state.highstate` executions

These steps ensure that the `salt-minion` agent is both configured correctly and applying desired states every 2 minutes.

While the above steps are useful for applying the current states, the whole point of continuous delivery is to deploy changes quickly. To do this we need to also keep the Salt states up-to-date.

#### Keeping Salt states up-to-date with Salt

One way to keep our Salt states up to date is to tell the `salt-minion` agent to update them for us.

Within the `/srv/salt/bencane/salt` directory exists a `states` directory that contains two files `base.sls` and `bencane.sls`. These two files both contain similar Salt states. Let's break down the contents of the `base.sls` file to understand what actions it's telling the `salt-minion` agent to perform.

```
$ cat salt/states/base.sls
/srv/salt/base:
  file.directory:
    - user: root
    - group: root
    - mode: 700
    - makedirs: True

base_states:
  git.latest:
    - name: https://github.com/madflojo/salt-base.git
    - target: /srv/salt/base
    - force: True
```

In the above we can see that the `base.sls` file contains two Salt states. The first is a `file` state that is set to ensure the `/srv/salt/base` directory exists with the defined permissions.

The second state is a bit more interesting as it is a `git` state which is set to pull the `latest` copy of the [salt-base](https://github.com/madflojo/salt-base.git) repository and clone it into `/srv/salt/base`.

With this state defined, every time the `salt-minion` agent runs (which is every 2 minutes via the `cron.d` job); the agent will check for new updates to the repository and deploy them to `/srv/salt/base`.

The `bencane.sls` file contains similar states, with the difference being the repository cloned and the location to deploy the state files to.

```
$ cat salt/states/bencane.sls
/srv/salt/bencane:
  file.directory:
    - user: root
    - group: root
    - mode: 700
    - makedirs: True

bencane_states:
  git.latest:
    - name: https://github.com/madflojo/blog-salt.git
    - target: /srv/salt/bencane
    - force: True
```

At this point, we now have a Masterless Salt Minion that is not only configured to "self-manage" it's own packages, but also the Salt state files that drive it.

As the state files within the `git` repositories are updated, those updates are then pulled from each Minion every 2 minutes. Whether that change is adding the `screen` package, or deploying a new Docker container; that change is deployed across many Masterless Minions all at once.

## What's next

With the above steps complete, we now have a method for taking a new server and turning it into a Self-Managed Masterless Minion. What we didn't cover however, is how to automate the initial installation and configuration.

In next months article, we will talk about using `salt-ssh` to automate the first time installation and configuration the `salt-minion` agent using the same Salt states we used today.

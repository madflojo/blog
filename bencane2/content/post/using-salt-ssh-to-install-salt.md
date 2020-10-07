---
authors:
- Benjamin Cane
categories:
- Linux
- SaltStack
date: '2016-07-19T17:30:00'
description: Using SaltStack's ability to run agentless over SSH to install the salt-minion
  agent
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- SaltStack
- salt-ssh
- salt-minion
- minion-less salt
- salt
title: Using salt-ssh to install Salt
url: /2016/07/19/using-salt-ssh-to-install-salt

---
In recent articles I covered how I've built a Continuous Delivery pipeline for my blog. These articles talk about [using Docker to build a container](http://bencane.com/2015/12/01/getting-started-with-docker-by-dockerizing-this-blog/) for my blog, [using Travis CI to test and build that container](http://bencane.com/2016/01/11/using-travis-ci-to-test-docker-builds/), and finally [using a Masterless SaltStack configuration](http://bencane.com/2016/03/22/self-managing-servers-with-masterless-saltstack-minions/) to deploy the blog. Once setup, this pipeline enables me to publish new posts by simply managing them within a GitHub repository.

The nice thing about this setup is that not only are blog posts managed hands-free. All of the servers that host my blog are managed hands-free. That means required packages, services and configurations are all deployed with the same Masterless SaltStack configuration used for the blog application deployment.

The only thing that isn't hands-free about this setup, is installing and configuring the initial SaltStack Minion agent. That is, until today. In this article I am going to cover how to use `salt-ssh`, SaltStack's SSH functionality to install and configure the `salt-minion` package on a new server.

## How `salt-ssh` works

A typical SaltStack deployment consists of a Master server running the `salt-master` process, and one or more Minion servers running the `salt-minion` process. The `salt-minion` service will initiate communication with the `salt-master` service over a **ZeroMQ** connection and the Master distributes desired states to the Minion.

With this typical setup, you must first have a `salt-master` service installed and configured, and every server that you wish to manage with Salt must have the `salt-minion` service installed and configured. The `salt-ssh` package however, changes that.

`salt-ssh` is designed to provide SaltStack with the ability to manage servers in an agent-less fashion. What that means is, `salt-ssh` gives you the ability to manage a server, without having to install and configure the `salt-minion` package.

### Why use `salt-ssh` instead of the `salt-minion` agent?

Why would anyone not want to install the `salt-minion` package? Well, there are a lot of possible reasons. One reason that comes to mind is that some systems are so performance oriented that there may be a desire to avoid performance degradation by running an agent. While `salt-minion` doesn't normally use a lot of resources, it uses some and that some may be too much for certain environments.

Another reason may be due to network restrictions, for example if the Minions are in a DMZ segment of a network you may want to use `salt-ssh` from the master so that connections are only going from the master to the minion and never the minion to the master like the traditional setup.

For today's article, the reasoning behind using `salt-ssh` is that I wish to automate the installation and configuration of the `salt-minion` service on **new servers**. These servers will not have the `salt-minion` package installed by default and I wanted to automate the initial installation of Salt.

## Getting started with `salt-ssh`

Before we can start using `salt-ssh` to setup our new server we will first need to setup a Master server where we can call `salt-ssh` from. For my environment I will be using a virtual machine running on my local laptop as the Salt Master. Since we are using `salt-ssh` there is no need for the Minions to connect to this Master which makes running it from a laptop a simple solution.

### Installing SaltStack

On this Salt Master, we will need to install both the `salt-master` and the `salt-ssh` packages. Like previous articles we will be following [SaltStack's official guide](https://docs.saltstack.com/en/latest/topics/installation/ubuntu.html) for installing Salt on Ubuntu systems.

#### Setup Apt

The official install guide for Ubuntu uses the Apt package manager to install SaltStack. In order to install these packages with Apt we will need to setup the SaltStack repository. We will do so using the `add-apt-repository` command.

```shell
$ sudo add-apt-repository ppa:saltstack/salt
     Salt, the remote execution and configuration management tool.
     More info: https://launchpad.net/~saltstack/+archive/ubuntu/salt
    Press [ENTER] to continue or ctrl-c to cancel adding it

    gpg: keyring `/tmp/tmpvi1b21hk/secring.gpg' created
    gpg: keyring `/tmp/tmpvi1b21hk/pubring.gpg' created
    gpg: requesting key 0E27C0A6 from hkp server keyserver.ubuntu.com
    gpg: /tmp/tmpvi1b21hk/trustdb.gpg: trustdb created
    gpg: key 0E27C0A6: public key "Launchpad PPA for Salt Stack" imported
    gpg: Total number processed: 1
    gpg:               imported: 1  (RSA: 1)
    OK
```

Once the Apt repository has been added we will need to refresh Apt's package cache with the `apt-get update` command.

```shell
$ sudo apt-get update
Get:1 http://security.ubuntu.com trusty-security InRelease [65.9 kB]
Ign http://ppa.launchpad.net trusty InRelease                                  
Ign http://archive.ubuntu.com trusty InRelease                                 
Get:2 http://archive.ubuntu.com trusty-updates InRelease [65.9 kB]
Get:3 http://ppa.launchpad.net trusty Release.gpg [316 B]                      
Get:4 http://ppa.launchpad.net trusty Release [15.1 kB]                        
Get:5 http://security.ubuntu.com trusty-security/main Sources [118 kB]         
Fetched 10.9 MB in 7s (1,528 kB/s)                                             
Reading package lists... Done
```

This update command causes Apt to look through it's known package repositories and refresh a local inventory of available packages.

#### Installing the `salt-master` and `salt-ssh` packages

Now that we have SaltStack's Apt repository configured we can proceed with installing the required Salt packages. We will do this with the `apt-get install` command specifying the two packages we wish to install.

```shell
$ sudo apt-get install salt-master salt-ssh
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following extra packages will be installed:
  git git-man liberror-perl libpgm-5.1-0 libzmq3 python-async python-croniter
  python-dateutil python-git python-gitdb python-jinja2 python-m2crypto
  python-markupsafe python-msgpack python-smmap python-zmq salt-common
Suggested packages:
  git-daemon-run git-daemon-sysvinit git-doc git-el git-email git-gui gitk
  gitweb git-arch git-bzr git-cvs git-mediawiki git-svn python-jinja2-doc
  salt-doc python-mako
The following NEW packages will be installed:
  git git-man liberror-perl libpgm-5.1-0 libzmq3 python-async python-croniter
  python-dateutil python-git python-gitdb python-jinja2 python-m2crypto
  python-markupsafe python-msgpack python-smmap python-zmq salt-common
  salt-master salt-ssh
0 upgraded, 19 newly installed, 0 to remove and 189 not upgraded.
Need to get 7,069 kB of archives.
After this operation, 38.7 MB of additional disk space will be used.
Do you want to continue? [Y/n] Y
```

In addition to the `salt-ssh` and `salt-master` packages Apt will install any dependencies that these packages require. With these packages installed, we can now move on to configuring our Salt master.

### Configuring `salt-ssh` to connect to our target minion

Before we can start using `salt-ssh` to manage our new minion server we will first need to tell `salt-ssh` how to connect to that server. We will do this by editing the `/etc/salt/roster` file.

```shell
$ sudo vi /etc/salt/roster
```

With a traditional SaltStack setup the minion agents would initiate the first connection to the Salt master. This first connection is the way the master service identifies new minion servers. With `salt-ssh` there is no process for Salt to automatically identify new minion servers. This is where the `/etc/salt/roster` file comes into the picture, as this file used as an inventory of minions for `salt-ssh`.

As with other configuration files in Salt, the `roster` file is a **YAML** formatted file which makes it fairly straight forwarder to understand. The information required to specify a new minion is also pretty straight forward.

```yaml+jinja
blr1-001:
  host: 10.0.0.2
  user: root
```

The above information is fairly minimal, the basic definition is a Target name `blr1-001`, a Hostname or IP address specified by `host` and then the Username specified by `user`.

The target name is used when running the `salt-ssh` command to specify what minion we wish to target. The `host` key is used by `salt-ssh` to define where to connect to, and the `user` key is used to define who to connect as.

In the example above I specified to use the `root` user. It is possible to use `salt-ssh` with a non-root user by simply adding `sudo: True` to the minion entry.

#### Testing connectivity to our minion

With the minion now defined within the `/etc/salt/roster` file we should now be able to connect to our minion with `salt-ssh`. We can test this out by executing a `test.ping` task against this target with `salt-ssh`.

```shell
$ sudo salt-ssh 'blr1-001' --priv=/home/vagrant/.ssh/id_rsa test.ping
blr1-001:
    ----------
    retcode:
        254
    stderr:
    stdout:
        The host key needs to be accepted, to auto accept run salt-ssh with the -i flag:
        The authenticity of host '10.0.0.2 (10.0.0.2)' can't be established.
        ECDSA key fingerprint is 2c:34:0a:51:a2:bb:88:cc:3b:86:25:bc:b8:d0:b3:d0.
        Are you sure you want to continue connecting (yes/no)?
```

The `salt-ssh` command above has a similar syntax to the standard `salt` command called with a typical Master/Minion setup; the format is `salt-ssh <target> <task>`. In this case our target was `blr1-001` the same name we defined earlier and our task was `test.ping`.

You may also notice that I passed the `--priv` flag followed by a path to my SSH private key. This flag is used to specify an SSH key to use when connecting to the minion server. By default, `salt-ssh` will use SaltStack's internal SSH key, which means if you wish to use an alternative key you will need to specify the key with the `--priv` flag.

In many cases it's perfectly fine to use SaltStack's internal SSH key, in my case the SSH public key has already been distributed which means I do not want to use Salt's internal SSH key.

#### Bypassing Host Key Validation

If we look at the output of the `salt-ssh` command executed earlier, we can see that the command was not successful. The reason for this is because this master server has not accepted the host key from the new minion server. We can get around this issue by specifying the `-i` flag when running `salt-ssh`.

```shell
$ sudo salt-ssh 'blr1-001' --priv /home/vagrant/.ssh/id_rsa -i test.ping
blr1-001:
    True
```

The `-i` flag tells `salt-ssh` to ignore host key checks from SSH. We can see from the above `salt-ssh` execution, when the `-i` flag is used, everything works as expected.

#### Specifying a password

In the `salt-ssh` commands above we used an SSH key for authentication with the Minion server. This worked because prior to setting up Salt, I deployed the public SSH key to the minion server we are connecting with. If we didn't want to use SSH keys for authentication with the Salt Minion for whatever reason, we could also use password based authentication by specifying the password within the `roster` file.

```shell
$ sudo vi /etc/salt/roster
```

To add a password for authentication, simply add the `passwd` key within the target servers specification.

```yaml+jinja
blr1-001:
  host: 10.0.0.2
  user: root
  passwd: example
```

With the above definition `salt-ssh` will now connect to our minion by establishing an SSH connection to `10.0.0.2` and login to this system as the `root` user with the password of `example`. With a password defined, we can rerun our `test.ping` this time with the `--priv` flag omitted.

```shell
$ sudo salt-ssh 'blr1-001' -i test.ping
blr1-001:
    True
```

Now that a `test.ping` has returned correctly we can move on to our next step of defining the Salt states to install and configure the `salt-minion` package.

### Using Salt to install Salt

In the [Master-less Salt Minions](http://bencane.com/2016/03/22/self-managing-servers-with-masterless-saltstack-minions/) article I had two GitHub repositories setup with various Salt state files. One repository contains salt state files that can be used to setup a [generic base system](https://github.com/madflojo/salt-base), and the other contains custom state files used to setup the [environment running this blog](https://github.com/madflojo/blog-salt).

#### Breaking down the minion state

Within this second repository is a salt state file that installs and configures the `salt-minion` service. Let's take a quick look at this state to understand how the `salt-minion` package is being installed.

```yaml+jinja
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

In the above state we can see that the Salt Apt repository is being added with the `pkgrep` module. The `salt-minion` package is being installed with the `pkg` module and the `salt-minion` service is being disabled by the `service` module.

We can also see that two files `/etc/salt/minion.d/masterless.conf` and `/etc/cron.d/salt-standalone` are being deployed. For this article, we will use this state as is to perform the initial `salt-minion` installation and configuration.

#### Setting up the master

As with the previous article we will use both of these repositories to setup our minion server. We will get started by first using `git` to clone these repositories into a directory within `/srv/salt`.

For the first repository, we will clone the contents into a `base` directory.

```shell
$ sudo git clone https://github.com/madflojo/salt-base.git /srv/salt/base
Cloning into '/srv/salt/base'...
remote: Counting objects: 54, done.
remote: Total 54 (delta 0), reused 0 (delta 0), pack-reused 54
Unpacking objects: 100% (54/54), done.
Checking connectivity... done.
```

The second repository we will clone into `/srv/salt/bencane`.

```shell
$ sudo git clone https://github.com/madflojo/blog-salt.git /srv/salt/bencane
Cloning into '/srv/salt/bencane'...
remote: Counting objects: 46, done.
remote: Total 46 (delta 0), reused 0 (delta 0), pack-reused 46
Unpacking objects: 100% (46/46), done.
Checking connectivity... done.
```

With all of the salt states now on our local system we can configure Salt to use these state files. To do this we will need to edit the `/etc/salt/master` configuration file.

```shell
$ sudo vi /etc/salt/master
```

Within the `master` file the `file_roots` configuration parameter is used to define where Salt's state files are located on the master. Since we have two different locations for the two sets of state files we will specify them individually as their own item underneath `file_roots`.

```yaml+jinja
file_roots:
  base:
    - /srv/salt/base
  bencane:
    - /srv/salt/bencane
```

With the above defined, we can now use our Salt states to setup a new minion server. To do this we will once again run `salt-ssh` but this time specifying the `state.highstate` task.


```shell
$ sudo salt-ssh 'blr1-001' -i state.highstate
----------
          ID: salt-minion
    Function: pkgrepo.managed
        Name: deb http://repo.saltstack.com/apt/ubuntu/14.04/amd64/latest trusty main
      Result: True
     Comment: Configured package repo 'deb http://repo.saltstack.com/apt/ubuntu/14.04/amd64/latest trusty main'
     Started: 21:18:54.462571
    Duration: 20440.965 ms
     Changes:   
              ----------
              repo:
                  deb http://repo.saltstack.com/apt/ubuntu/14.04/amd64/latest trusty main
----------
          ID: salt-minion
    Function: pkg.latest
      Result: True
     Comment: The following packages were successfully installed/upgraded: salt-minion
     Started: 21:19:14.903859
    Duration: 16889.713 ms
     Changes:   
              ----------
              dctrl-tools:
                  ----------
                  new:
                      2.23ubuntu1
                  old:
              salt-minion:
                  ----------
                  new:
                      2016.3.1+ds-1
                  old:
----------
          ID: salt-minion
    Function: service.dead
      Result: True
     Comment: Service salt-minion has been disabled, and is dead
     Started: 21:19:32.488449
    Duration: 133.722 ms
     Changes:   
              ----------
              salt-minion:
                  True
----------
          ID: /etc/salt/minion.d/masterless.conf
    Function: file.managed
      Result: True
     Comment: File /etc/salt/minion.d/masterless.conf updated
     Started: 21:19:32.626328
    Duration: 11.762 ms
     Changes:   
              ----------
              diff:
                  New file
              mode:
                  0644
----------
          ID: /etc/cron.d/salt-standalone
    Function: file.managed
      Result: True
     Comment: File /etc/cron.d/salt-standalone updated
     Started: 21:19:32.638297
    Duration: 4.049 ms
     Changes:   
              ----------
              diff:
                  New file
              mode:
                  0644

Summary
-------------
Succeeded: 37 (changed=23)
Failed:     0
-------------
Total states run:     37
```

From the results of the `state.highstate` task, we can see that `37` Salt states were verified and `23` of those resulted in changes being made. We can also see from the output of the command above that our `salt-ssh` execution just resulted in the installation and configuration of the `salt-minion` package.

If we wanted to verify that this is true even further we can use the `cmd.run` Salt module to execute the `dpkg --list` command.

```shell
$ sudo salt-ssh 'blr1-001' -i cmd.run "dpkg --list | grep salt"
blr1-001:
    ii  salt-common                        2016.3.1+ds-1                    all          shared libraries that salt requires for all packages
    ii  salt-minion                        2016.3.1+ds-1                    all          client package for salt, the distributed remote execution system
```

## Summary

With the above, we can see that we were successfully able to install the `salt-minion` agent to a remote system via `salt-ssh`. While this may seem like quite a bit of work to setup for a single minion. The ability to install Salt with `salt-ssh` can be very useful when you are setting up multiple minions, as this same methodology works whether you're installing Salt on 1 or 1,000 minions.

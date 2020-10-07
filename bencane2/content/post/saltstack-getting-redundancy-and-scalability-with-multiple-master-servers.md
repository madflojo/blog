---
authors:
- Benjamin Cane
categories:
- Linux
- SaltStack
- High Availability
date: '2014-02-04T08:00:00'
description: A how to article on setting up multiple saltstack master servers for
  redundancy and scalability. With SaltStack you can easily setup 2 or more master
  servers in a round robin configuration to provide high availability and scalability
  to your infrastructure automation tools.
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- redhat
- ubuntu
- saltstack
- saltstack ha
- high availability
- multiple masters
- infrastructure automation
title: 'SaltStack: Getting redundancy and scalability with multiple master servers'
url: /2014/02/04/saltstack-getting-redundancy-and-scalability-with-multiple-master-servers

---

Today's article is an item I covered briefly during my presentation at SaltConf 2014 (which was a pretty awesome conference by the way). One of the lesser known features of SaltStack is the ability to configure multiple master servers. Having an additional master server allows for some extra redundancy as well as capacity for large implementations. While I covered the benefits of having an additional master server in my presentation I didn't cover in full detail how to set this up, today I will cover the details of configuring multiple salt masters.

## How SaltStack multi-master works

SaltStack's multiple master configuration is actually a pretty simple implementation. The master servers do not require any communication or heartbeats between each other, both servers are simply online at the same time. This allows minions to communicate to either master server without any special DNS or IP fail-over mechanisms. The only prerequisite is that the two masters must share the same public/private keys.

During initial setup master and minion servers exchange public keys, this is to prevent any spoofing since many times servers are identified by hostname. At this time minions cannot store more than 1 master server key, this means that each master server in a multi-master setup must present the same public key to the minion/minions.

Once they keys are setup properly the minion will round robin requests between the two master servers allowing for both redundancy; in case of failures, and scalability for systems that require more than one master server.

## Setting up the multi-master environment

The installation steps for a multi-master environment is not very difference from a regular master-minion implementation. The order of installation is fairly important, the steps below are ordered in order to allow an easy key synchronization between the two masters, as well as the minion servers. In theory you can execute these steps in a different order but you should keep a keen eye on the direction that keys are being exchanged, the key exchange will either make or break the multi-master implementation.

### Installing salt-master on master1

#### Installing Python Software Properties or Software Properties Common

SaltStack maintains a PPA (Personal Package Archive) that can be added as an apt repository. To add a PPA repository it may be necessary to install either the `python-software-properties` package for earlier Ubuntu versions and `software-properties-common` for newer Ubuntu releases.

**Pre 12.10**

    root@master1:~# apt-get --yes -q install python-software-properties

**Post 12.10**

    root@master1:~# apt-get --yes -q install software-properties-common

#### Adding the SaltStack PPA repository

    root@master1:~# add-apt-repository ppa:saltstack/salt
    You are about to add the following PPA to your system:
     Salt, the remote execution and configuration management tool.
     More info: https://launchpad.net/~saltstack/+archive/salt
    Press [ENTER] to continue or ctrl-c to cancel adding it

Make sure that you press **[ENTER]** otherwise the repository will not be added.

#### Update apt's package indexes

After adding the repository make sure that you update `apt`'s package index.

    root@master1:~# apt-get --yes -q update

#### Install the salt-master package

At this point we can install the `salt-master` package on the first master server `master1`.

    root@master1:~# apt-get --yes -q install salt-master

### Installing salt-master on master2

These next steps are repeated steps of installing the `salt-master` package, if you can install SaltStack with your eyes closed you may want to skip to the next section.

#### Installing Python Software Properties or Software Properties Common

SaltStack maintains a PPA (Personal Package Archive) that can be added as an apt repository. To add a PPA repository it may be necessary to install either the `python-software-properties` package for earlier Ubuntu versions and `software-properties-common` for newer Ubuntu releases.

**Pre 12.10**

    root@master2:~# apt-get --yes -q install python-software-properties

**Post 12.10**

    root@master2:~# apt-get --yes -q install software-properties-common

#### Adding the SaltStack PPA repository

    root@master2:~# add-apt-repository ppa:saltstack/salt
    You are about to add the following PPA to your system:
     Salt, the remote execution and configuration management tool.
     More info: https://launchpad.net/~saltstack/+archive/salt
    Press [ENTER] to continue or ctrl-c to cancel adding it

Make sure that you press **[ENTER]** otherwise the repository will not be added.

#### Update apt's package indexes

After adding the repository make sure that you update `apt`'s package index.

    root@master2:~# apt-get --yes -q update

#### Install the salt-master package

At this point we can install the `salt-master` package on the secondary master server `master2`.

    root@master2:~# apt-get --yes -q install salt-master

### Synchronizing the master servers

#### Copy the master key from master1

Both master servers must have the same `master.pem` and `master.pub` keys, the `master.pub` key is the public key sent to the minions and the `master.pem` is the private key stored on the master itself. If you do not have both of these key files the same on both master servers, the minion will error and abort during setup. It is a good idea to have these keys copied before attaching any minions. After the keys are copied restart the `salt-master` service.

    root@master2:~# scp 10.0.3.61:/etc/salt/pki/master/master.pem /etc/salt/pki/master/
    root@master2:~# scp 10.0.3.61:/etc/salt/pki/master/master.pub /etc/salt/pki/master/
    root@master2:~# service salt-master restart

If you are adding a second master server to an existing environment, it is best to make sure that you copy the `master.pem` and `master.pub` files from your existing master. Otherwise you will need to remove a file from each and every minion server and restart the minion process.

#### Keeping the file and pillar roots in sync

While it is not required it is advisable to keep the `file_roots` and `pillar_roots` directories in sync between the two master servers. This ensures that any changes to the pillars or state files are the same for both master servers. Not keeping these in sync can lead to many head scratching moments where the state file is defined properly but the minion is not picking up the changes. 

In my example I am simply using `rsync` to keep the directories in sync between to master servers, while this is fine for small implementations that don't change much. This solution may not be scalable for large or frequently updated salt implementations. For those environments it is advisable to use a solution such as a clustered, replicated or shared file system. There are many good file systems to choose from and the decision on which file system would be better is going to depend on how available this system needs to be. If you don't have any concerns with losing both masters at the same time a solution such as NFS would be easy, if you absolutely must have one master up no matter what than a solution such as glusterFS may be a better choice.

For this example though, `rsync` works just fine.

    root@master2:/# rsync -avzr srv 10.0.3.61:/
    root@10.0.3.61's password: 
    sending incremental file list
    srv/
    srv/salt/
    srv/salt/top.sls
    srv/salt/screen/
    srv/salt/screen/init.sls
    srv/pillar_roots/
    srv/pillar_roots/top.sls
    srv/pillar_roots/multimaster/
    srv/pillar_roots/multimaster/init.sls
    
    sent 524 bytes  received 108 bytes  180.57 bytes/sec
    total size is 105  speedup is 0.17

The `rsync` command above shows the /srv directory being copied, this is the default directory for `file_roots` and `pillar_roots`. If you modify the path for these directories you will need to adjust the `rsync` command appropriately.

### Installing salt-minion on minion

Installation of a multi-master minion is no different than a single master minion installation, the only differences are during the configuration steps.

#### Installing Python Software Properties or Software Properties Common

SaltStack maintains a PPA (Personal Package Archive) that can be added as an apt repository. To add a PPA repository it may be necessary to install either the `python-software-properties` package for earlier Ubuntu versions and `software-properties-common` for newer Ubuntu releases.

**Pre 12.10**

    root@minion1:~# apt-get --yes -q install python-software-properties

**Post 12.10**

    root@minion1:~# apt-get --yes -q install software-properties-common

#### Adding the SaltStack PPA repository

    root@minion1:~# add-apt-repository ppa:saltstack/salt
    You are about to add the following PPA to your system:
     Salt, the remote execution and configuration management tool.
     More info: https://launchpad.net/~saltstack/+archive/salt
    Press [ENTER] to continue or ctrl-c to cancel adding it

Make sure that you press **[ENTER]** otherwise the repository will not be added.

#### Update apt's package indexes

After adding the repository make sure that you update `apt`'s package index.

    root@minion1:~# apt-get --yes -q update

#### Install the salt-minion package

At this point we can install the `salt-minion` package

    root@minion1:~# apt-get --yes -q install salt-minion

### Configure the minion server

Now that we have the 2 master servers synchronized and the minion server installed, we will need to configure the minion to talk to both master servers.

#### Define multiple masters

To tell the minion to use both master servers is similar to the way you would configure a single master, we will need to edit the `/etc/salt/minion` configuration file and specify the two master servers.

    root@minion1:~# vi /etc/salt/minion

**Find:**

    #master: salt

**Replace with:**

    master:
      - 10.0.3.61 # master1
      - 10.0.3.230 # master2

#### Restart the minion service

After editing the minion configuration file you will need to restart the `salt-minion` service. During restart the minion will send it's public key to the master servers.

    root@minion1:~# service salt-minion restart

#### Accept the minions keys on both master servers

While it is possible to synchronize the `/etc/salt/pki/master` directories between the two master servers, in my example I am simply going to accept the minion keys on both master servers independently. The scale of your implementation will dictate whether or not you should do this, but in many environments accepting the keys is a one time process. If you are using `salt-cloud` or anything to auto accept the keys it might be easier to keep the `/etc/salt/pki/master` directories synchronized as any key accepted on one master would then be accepted for both.

On my test setup during the initial start of `salt-minion`, the minions key was sent to `master2` for authentication first.

    root@master2:/# salt-key -a minion1
    The following keys are going to be accepted:
    Unaccepted Keys:
    minion1
    Proceed? [n/Y] y
    Key for minion minion1 accepted.

After accepting the key on `master2`, the minion key was not present on `master1`. In order to force the minion to send the key to `master1` I ran a `salt-call` from the minion knowing it could fail if it tried to sync with `master1`.

    root@minion1:~# salt-call state.highstate
    Minion failed to authenticate with the master, has the minion key been accepted?

After the failed `salt-call` I was able to accept the key on `master1` as well.

    root@master1:~# salt-key -a minion1
    The following keys are going to be accepted:
    Unaccepted Keys:
    minion1
    Proceed? [n/Y] y
    Key for minion minion1 accepted.

## Testing the multi-master setup

Now that the 2 master servers are setup and all of the keys are accepted we can start testing the setup to ensure everything is working correctly.

### Running a salt-call from the minion

The first test I run is usually a `highstate` from the minion. This is a good way to ensure all of your state files are defined and found correctly. This also tests that you were successful in synchronizing the file and pillar roots directories. I suggest running this test multiple times to ensure that it works against both master servers.

    root@minion1:~# salt-call state.highstate
    <truncated output>
    local:
    ----------
        State: - pkg
        Name:      screen
        Function:  installed
            Result:    True
            Comment:   The following packages were installed/updated: screen.
            Changes:   screen: { new : 4.0.3-14ubuntu10
    old : 
    }
                       
    
    Summary
    ------------
    Succeeded: 1
    Failed:    0
    ------------
    Total:     1

### Running test.ping from the masters

Another good test to run is to make sure that both master servers are able to ping the minion, this can be done with `test.ping`

**master1**

    root@master1:/srv# salt '*' test.ping
    minion1:
        True

**master2**

    root@master2:/srv# salt '*' test.ping
    minion1:
        True

This tells us that both master servers are able to communicate and authenticate with the minion.

## Adding additional master servers

There is no hard limit on the number of master servers, if you wanted you could add a third, fourth or twentieth using the same processes as above. Simply repeat the steps as necessary, and make sure to synchronize all of the keys and state/pillar files. If you are scaling your master servers to a large number you may want to consider setting up a shared/replicated file-system for the state/pillar files as well as the minion keys.

As you can see the setup of a multi-master environment is pretty simple. If correctly implemented SaltStack's multi-master configuration can easily meet high availability requirements or provide extra capacity.

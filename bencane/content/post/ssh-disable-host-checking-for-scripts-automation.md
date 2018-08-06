---
authors:
- Benjamin Cane
categories:
- Administration
- How To and Tutorials
- Programming
- Security
- Shell Scripting
date: '2013-07-22T14:00:26'
description: How to disable SSH host checking for both scripts and lazy users
draft: false
header:
  caption: ''
  image: ''
tags:
- bash
- known hosts file
- known_hosts
- linux
- linux os
- red hat os
- rsa key
- shell
- shell scripting
- ssh
- ssh keys
- ssh-keygen
title: 'SSH: Disable Host Checking for Scripts & Automation'
url: /2013/07/22/ssh-disable-host-checking-for-scripts-automation

---

In the world of Cloud Servers and Virtual Machines scripting and automation are top priority for any sysadmin. Recently while I was creating a script that logged into another server via SSH to run arbitrary commands, I ran into a brick wall.

    $ ssh 192.168.0.169
    The authenticity of host '192.168.0.169 (192.168.0.169)' can't be established.
    ECDSA key fingerprint is 74:39:3b:09:43:57:ea:fb:12:18:45:0e:c6:55:bf:58.
    Are you sure you want to continue connecting (yes/no)?

To anyone who has used SSH long enough the above message should look familiar. Everytime a user logs into a host via SSH that hosts unique host key is stored in the users `~/.ssh/known_hosts` file. If a host is not already added into this file than the first occurrence of an SSH connection will display the above message, prompting the user to either enter yes or no. By entering Yes, the servers unique host key is automatically stored into the `known_hosts` file, this has been implemented to prevent man in the middle attacks.

Since servers are practically dispensable these days, they are provisioned and re-provisioned at the click of a button. It is quite common for a script to perform a remote SSH login on a new system to run commands. If this script is being run by an automated process, being asked a question may prevent the script from executing.

To get around this you can disable this feature, called `StrictHostKeyChecking`.

## Disable StrictHostKeyChecking System Wide

StrictHostKeyChecking can be disabled on both the system as a whole or on a per user basis. To disable this setting on the system simply modify the `/etc/ssh/ssh_config` file.

    # vi /etc/ssh/ssh_config

**Find:**

    # StrictHostKeyChecking ask

**Replace With:**

    StrictHostKeyChecking no

## Disable StrictHostKeyChecking Per User

Since StrictHostKeyChecking is enabled by default to prevent man-in-the-middle attacks it is generally a good idea to only disable it on a per user basis. This can be accomplished by editing the `.ssh/config` file in each users home directory.

    # vi ~/.ssh/config

**Append:**

    StrictHostKeyChecking no

## Disabling the KnownHostsFile

If a host key is already added to the known_hosts file but does not match the host key being presented to SSH on login, the login will still fail. This would prevent logging into a host that shares the same hostname/IP as a previously provisioned host.

To prevent this scenario from stopping your automated script you can also change the KnownHostsFile to `/dev/null`. Thus preventing the host key from being added to any real file.

    # vi ~/.ssh/config

**Append:**

    UserKnownHostsFile /dev/null

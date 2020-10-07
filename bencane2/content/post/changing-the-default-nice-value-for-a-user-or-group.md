---
authors:
- Benjamin Cane
categories:
- All Articles
- How To and Tutorials
- Linux
- Linux Commands
date: '2013-09-30T14:53:19'
description: How to make a niceness value default for any user or group using /etc/security/limits.conf
draft: false
header:
  caption: ''
  image: ''
tags:
- linux os
- linux server
- linux system
- linux tutorial
- nice
- niceness
title: Changing the default nice value for a user or group
url: /2013/09/30/changing-the-default-nice-value-for-a-user-or-group

---

Recently I covered[how to increase and decrease the CPU priority of processes using nice and renice](http://bencane.com/2013/09/09/setting-process-cpu-priority-with-nice-and-renice/). Today I am going to cover how to change the default niceness value for a user or group.

## Why change the default CPU priority value?

Before explaining how to change the default niceness value, let's cover why this could be useful.

### Scenario #1

You have a system that has thousands of users that log in via SSH and could potentially run CPU intensive tasks. By making the niceness value higher you will ensure that critical system processes will get higher CPU priority than the jobs ran by the users.

### Scenario #2

You have a production system that is sensitive to CPU spikes and want to ensure that one application has a higher priority than other applications or people users. By setting a lower niceness value for your important application you can advise the kernel to give that application users processes a higher priority.

While not every system needs this level of control; there are scenarios where it makes sense to give some processes higher priority than others.

## Changing the default niceness value

To set the default niceness value for a specific user we will use the `/etc/security/limits.conf` file.

### Setting the default priority on a user

    # vi /etc/security/limits.conf

**Append:**

    madflojo soft priority 5

All new logins from the user madflojo will now receive a niceness value of 5.

### Setting the default priority on a group

    # vi /etc/security/limits.conf

**Append:**

    @users soft priority 5

From this point all new logins by the users in the users group will also receive a niceness value of 5.

    $ nice
    0
    $ ssh localhost
    Warning: Permanently added 'localhost' (ECDSA) to the list of known hosts.
    madflojo@localhost's password:
    $ nice
    5

That's it, that is all of the editing required to change the default priority for users and groups. This value can be positive or negative and does not impact the ability of a user to adjust the niceness of processes to a "nicer" value.

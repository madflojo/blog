---
authors:
- Benjamin Cane
categories:
- Linux
date: '2014-08-18T14:45:00'
description: Removing an installed package with apt-get isn't as straight forward
  as you would think. This article walks you through removing a package the right
  way to allow for re-installation later and how to fix when an install will not deploy
  configuration files.
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- debian
- ubuntu
- apt-get
- apt
- package managers
- installing packages
- apt-get configuration files
title: Removing packages and configurations with apt-get
url: /2014/08/18/removing-packages-and-configurations-with-apt-get

---

Yesterday while re-purposing a server I was removing packages with `apt-get` and stumbled upon an interesting problem. After I removed the package and all of it's configurations, the subsequent installation did not re-deploy the configuration files.

After a bit of digging I found out that there are two methods for removing packages with `apt-get`. One of those method should be used if you want to remove binaries, and the other should be used if you want to remove both binaries and configuration files.

## What I did

Since the method I originally used caused at least 10 minutes of head scratching; I thought it would be useful to share what I did and how to resolve it.

On my system the package I wanted to remove was `supervisor` which is [pretty awesome btw](http://supervisord.org/). To remove the package I simply removed it with `apt-get remove` just like I've done many times before.
    
    # apt-get remove supervisor
    Reading package lists... Done
    Building dependency tree       
    Reading state information... Done
    The following packages will be REMOVED:
      supervisor
    0 upgraded, 0 newly installed, 1 to remove and 0 not upgraded.
    After this operation, 1,521 kB disk space will be freed.
    Do you want to continue [Y/n]? y
    (Reading database ... 14158 files and directories currently installed.)
    Removing supervisor ...
    Stopping supervisor: supervisord.
    Processing triggers for ureadahead ...

No issues so far, the package was removed according to `apt` without any issues. However, after looking around a bit I noticed that the `/etc/supervisor` directory still existed. As well as the `supervisord.conf` file. 

    # ls -la /etc/supervisor
    total 12
    drwxr-xr-x  2 root root 4096 Aug 17 19:44 .
    drwxr-xr-x 68 root root 4096 Aug 17 19:43 ..
    -rw-r--r--  1 root root 1178 Jul 30  2013 supervisord.conf

Considering I was planning on re-installing `supervisor` and I didn't want to cause any weird configuration issues as I moved from one server role to another I did what any other reasonable Sysadmin would do. I removed the directory...

    # rm -Rf /etc/supervisor

I knew the supervisor package was removed, and I assumed that the package didn't remove the config files to avoid losing custom configurations. In my case I wanted to start over from scratch, so deleting the directory sounded like a reasonable thing.

    # apt-get install supervisor
    Reading package lists... Done
    Building dependency tree       
    Reading state information... Done
    The following NEW packages will be installed:
      supervisor
    0 upgraded, 1 newly installed, 0 to remove and 0 not upgraded.
    Need to get 0 B/314 kB of archives.
    After this operation, 1,521 kB of additional disk space will be used.
    Selecting previously unselected package supervisor.
    (Reading database ... 13838 files and directories currently installed.)
    Unpacking supervisor (from .../supervisor_3.0b2-1_all.deb) ...
    Processing triggers for ureadahead ...
    Setting up supervisor (3.0b2-1) ...
    Starting supervisor: Error: could not find config file /etc/supervisor/supervisord.conf
    For help, use /usr/bin/supervisord -h
    invoke-rc.d: initscript supervisor, action "start" failed.
    dpkg: error processing supervisor (--configure):
     subprocess installed post-installation script returned error exit status 2
    Errors were encountered while processing:
     supervisor
    E: Sub-process /usr/bin/dpkg returned an error code (1)

However, it seems supervisor could not start after re-installing.

    # ls -la /etc/supervisor
    ls: cannot access /etc/supervisor: No such file or directory

There is good reason why `supervisor` wouldn't restart; because the `/etc/supervisor/supervisord.conf` file was missing. Shouldn't the package installation deploy the `supervisord.conf` file? Well, technically no. Not with the way I removed the `supervisor` package.

## Why it didn't work

### How remove works

If we look at `apt-get`'s man page a little closer we can see why the configuration files are still there.

    remove
      remove is identical to install except that packages are removed
      instead of installed. Note that removing a package leaves its
      configuration files on the system. 

As the manpage clearly says, remove will remove the package but leaves configuration files in place. This explains why the `/etc/supervisor` directory was lingering after removing the package; but it doesn't explain why a subsequent installation doesn't re-deploy the configuration files.

### Package States

If we use `dpkg` to look at the `supervisor` package, we will start to see the issue.

    # dpkg --list supervisor
    Desired=Unknown/Install/Remove/Purge/Hold
    | Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
    |/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
    ||/ Name                             Version               Architecture          Description
    +++-================================-=====================-=====================-========================================
    rc  supervisor                       3.0b2-1               all                   A system for controlling process state

With the `dpkg` package manager a package can have more states than just being installed or not-installed. In fact there are several package states with `dpkg`.

* **not-installed** - The package is not installed on this system
* **config-files** - Only the configuration files are deployed to this system
* **half-installed** - The installation of the package has been started, but not completed
* **unpacked** - The package is unpacked, but not configured
* **half-configured** - The package is unpacked and configuration has started but not completed
* **triggers-awaited** - The package awaits trigger processing by another package
* **triggers-pending** - The package has been triggered
* **installed** - The packaged is unpacked and configured OK

If you look at the first column of the `dpkg --list` it shows `rc`. The `r` in this column means the package is `remove`, which as we saw above means the configuration files are left on the system. The `c` in this column shows that the package is in the state of `config-files`. Meaning, only the configuration files are deployed on this system.

When running `apt-get install` the `apt` package manager will lookup the current state of the package, when it sees that the package is already in the `config-files` state it simply skips the configuration file portion of the package installation. Since I manually removed the configuration files outside of the `apt` or `dpkg` process the configuration files are gone and will not be deployed with a simple `apt-get install`.
    
## How to resolve it and remove configurations properly

### Purging the package from my system

At this point, I found myself with a broken installation of `supervisor`. Luckily, we can fix the issue by using the `purge` option of `apt-get`. 
    
    # apt-get purge supervisor
    Reading package lists... Done
    Building dependency tree       
    Reading state information... Done
    The following packages will be REMOVED:
      supervisor*
    0 upgraded, 0 newly installed, 1 to remove and 0 not upgraded.
    1 not fully installed or removed.
    After this operation, 1,521 kB disk space will be freed.
    Do you want to continue [Y/n]? y
    (Reading database ... 14158 files and directories currently installed.)
    Removing supervisor ...
    Stopping supervisor: supervisord.
    Purging configuration files for supervisor ...
    dpkg: warning: while removing supervisor, directory '/var/log/supervisor' not empty so not removed
    Processing triggers for ureadahead ...
    
### Purge vs Remove

The `purge` option of `apt-get` is similar to the `remove` function however with one difference. The `purge` option will remove both the package and configurations. After running `apt-get purge` we can see that the package was fully removed by running `dpkg --list` again.

    # dpkg --list supervisor
    dpkg-query: no packages found matching supervisor

### Re-installation without error

Now that the package has been fully purged, and the state of it is now `not-installed`; we can re-install without errors.
    
    # apt-get install supervisor
    Reading package lists... Done
    Building dependency tree       
    Reading state information... Done
    The following NEW packages will be installed:
      supervisor
    0 upgraded, 1 newly installed, 0 to remove and 0 not upgraded.
    Need to get 0 B/314 kB of archives.
    After this operation, 1,521 kB of additional disk space will be used.
    Selecting previously unselected package supervisor.
    (Reading database ... 13833 files and directories currently installed.)
    Unpacking supervisor (from .../supervisor_3.0b2-1_all.deb) ...
    Processing triggers for ureadahead ...
    Setting up supervisor (3.0b2-1) ...
    Starting supervisor: supervisord.
    Processing triggers for ureadahead ...

As you can see from the output above, the `supervisor` package has been installed and started. If we check the `/etc/supervisor` directory again we can also see the necessary configuration files.

    # ls -la /etc/supervisor/
    total 16
    drwxr-xr-x  3 root root 4096 Aug 17 19:46 .
    drwxr-xr-x 68 root root 4096 Aug 17 19:46 ..
    drwxr-xr-x  2 root root 4096 Jul 30  2013 conf.d
    -rw-r--r--  1 root root 1178 Jul 30  2013 supervisord.conf

## You should probably just use purge in most cases

After running into this issue I realized, most of the times I ran `apt-get remove` I really wanted the functionality of `apt-get purge`. While it is nice to keep configurations handy in case we need them after re-installation, using `remove` all the time also leaves random config files to clutter your system. Free to cause configuration issues when packages are removed then re-installed.

In the future I will most likely default to `apt-get purge`.

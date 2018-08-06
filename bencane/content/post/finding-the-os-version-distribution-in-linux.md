---
authors:
- Benjamin Cane
categories:
- Command Line
- How To and Tutorials
- Linux Commands
- Linux Distributions
- Red Hat
- SysAdmin Basics
- Ubuntu
date: '2013-08-28T06:08:03'
description: A simple trick on finding out the OS version and Distribution of a Linux
  system you have command line access to
draft: false
header:
  caption: ''
  image: ''
tags:
- config
- debian
- kernel version
- linux
- linux os
- linux version
- lsb-release
- os version
- red hat linux
- red hat os
- redhat
- redhat-release
- release
- scripts
- ubuntu
- ubuntu linux
title: Finding the OS version and Distribution in Linux
url: /2013/08/28/finding-the-os-version-distribution-in-linux

---

When supporting systems you have inherited or in environments that have many different OS versions and distributions of Linux. There are times when you simply don't know off hand what OS version or distribution the server you are logged into is.

Luckily there is a simple way to figure that out.

## Ubuntu/Debian

    $ cat /etc/lsb-release 
    DISTRIB_ID=Ubuntu
    DISTRIB_RELEASE=13.04
    DISTRIB_CODENAME=raring
    DISTRIB_DESCRIPTION="Ubuntu 13.04"

## RedHat/CentOS/Oracle Linux

    # cat /etc/redhat-release
    Red Hat Enterprise Linux Server release 5 (Tikanga)

## Catchall

If you are looking for a quick way and don't care what the output looks like, you can simply do this as well.

    $ cat /etc/*-release
    DISTRIB_ID=Ubuntu
    DISTRIB_RELEASE=13.04
    DISTRIB_CODENAME=raring
    DISTRIB_DESCRIPTION="Ubuntu 13.04"
    NAME="Ubuntu"
    VERSION="13.04, Raring Ringtail"
    ID=ubuntu
    ID_LIKE=debian
    PRETTY_NAME="Ubuntu 13.04"
    VERSION_ID="13.04"
    HOME_URL="http://www.ubuntu.com/"
    SUPPORT_URL="http://help.ubuntu.com/"
    BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"

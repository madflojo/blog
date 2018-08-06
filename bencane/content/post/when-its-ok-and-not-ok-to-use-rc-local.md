---
authors:
- Benjamin Cane
categories:
- Administration
- Best Practices
- FreeBSD
- Linux
- Unix
- Unix Distributions
date: '2011-12-30T09:30:25'
description: An article that discusses when it is appropriate and when it is not appropriate
  to use the rc.local file. A file that has been depreciated in some Linux distributions.
draft: false
header:
  caption: ''
  image: ''
tags:
- bsd
- debian
- freebsd
- init
- linkedin
- linux
- linux os
- linux server
- os x
- rc auto
- red hat linux
- solaris
- System V
- tech
- unix
title: When it's Ok and Not Ok to use rc.local
url: /2011/12/30/when-its-ok-and-not-ok-to-use-rc-local

---

On System V based OS's the `/etc/rc.local` file is executed by the init process at the end of the systems boot process. The fact that the rc.local file is executed during the boot process makes it an easy target for misuse by lazy Sysadmins. Since I started my Unix experience on FreeBSD which relies primarily on the `/etc/rc.*` configuration files, I've seen and shamefully contributed to my fair share of misuse in the rc.local file. However now that I've "grown up" as a Sysadmin the misuse of the `/etc/rc.local` file is now one of my pet peeves. Hopefully this article will explain to the unaware of when and why you should use the rc.local file.

## When it is Not Ok to use the /etc/rc.local file

The following are examples of rc.local misuse that I have seen with my own eyes. Usually this is caused by either a lack of understanding or just the lazy nature of a Sysadmin.

### Starting an Application/Service

I've seen this many times, in fact when I was googling around for examples of rc.local I found an example where someone put the instructions needed to start apache into the `/etc/rc.local` file.

**Why this is bad: **The rc.local file may start up your service just fine, but when the system is shutting down the init process will not stop your application gracefully. If your application uses lock files this may mean your application doesn't start on the next boot. In cases of applications it is always best to create an init script (or alternative depending on your distro i.e. Upstart or Systemd).

### Firewall rules

This is another popular case that people use the rc.local file. I've seen this on Linux and FreeBSD where people will put IPTABLES/IPFW rules in the rc.local file.

**Why this is bad:** Well to be frank, this isn't the correct place for these rules. In Linux you will have some sort of rules file; for example in Red Hat the configuration file is in `/etc/sysconfig/iptables`. It is better to use this file for many reasons one of which is when you perform a `service iptables restart` the rules specified in the iptables file will be readded. If they are specified in the rc.local file, they are only added during boot.

The same rings true with FreeBSD and IPFW, in FreeBSD the configuration file is `/etc/rc.firewall`. Within this file you can set your configuration to put all of your ipfw commands in a shell script. Depending on your scripting skills this can be a really easy way to enable and disable your firewall rules. Even if your scripting is not up to par you should still use the `/etc/rc.firewall` to define your firewall rules.

### Network Configuration

While I don't believe I've seen anyone do this with Linux, I know I have seen people add IP and Static route configuration commands in the rc.local file with FreeBSD.

**Why this is bad:** Again I'm going to use the reasoning of this isn't the correct place; all networking configuration should be configured in the rc.conf file. The rc.conf file is the documented home for this type of configuration, however on this I will admit I could be convinced that there are some cases where it is better to use the rc.local file.

The rc.conf file is a core configuration file in FreeBSD. If someone wanted to create a generic rc.conf file and deployed it to all of their servers but put host specific information into the rc.local; I could be convinced that this solution is easier than maintaining multiple rc.conf files and potentially having servers configured differently.

## When it is Ok to use the /etc/rc.local file

Whenever presented with the question of adding a command to the rc.local file, I ask myself these questions.
	
  * Is the command able to be performed by manipulating a configuration file such as `httpd.conf`, `sysctl`, `/etc/profile` or `ifcfg-eth0`?
    * Yes, Than put it in that configuration file.
    * No, Continue to next question.
  * Does the command start a service?
    * Yes, Than create a init, upstart, or systemd script to properly manage this service.
    * No, Continue to next question.
  * Is this command or commands related to an existing service?
    * Yes, Add these commands to the existing start script.
    * No, Proceed to editing the rc.local file.

It is very rare that I run into a task that cannot be added to a start script or configuration file, the only good example I have seen is when modifying some of the parameters defined in the `/proc` filesystem in Linux. There are a few things in the `/proc` filesystem that can only be modified by changing the values of the files within `/proc`. In these cases it is Ok to add the lines to the rc.local file.

_***Note: The Debian distribution of Linux does not even support the use of rc.local**_

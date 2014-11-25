---
author: bencane
comments: true
date: 2011-09-08 20:01:06+00:00
popularity: None
slug: mount-disabling-execution-of-scripts
title: 'mount: Disabling execution of scripts'
post_id: 48
categories:
- Administration
- Best Practices
- How To &amp; Tutorials
- Linux
- Linux Commands
- Security
tags:
- linux
- tech
- unix
---

One of the common ways of securing your system is by making the /tmp filesystem unable to run executables. This prevents users from executing scripts in /tmp which is generally writable by everyone.

You can restrict this with the mount option noexec.

**Here is an example:**

    [root@bcane playground]# mount | grep play  
    /dev/mapper/vgfirst-lv_test1 on /var/tmp/playground type ext3 (rw)  
    [root@bcane playground]# ./helloworld.sh   
    Hello World  
    [root@bcane playground]# mount -o remount,noexec /dev/mapper/vgfirst-lv_test1 /var/tmp/playground  
    [root@bcane playground]# mount | grep play  
    /dev/mapper/vgfirst-lv_test1 on /var/tmp/playground type ext3 (rw,noexec)  
    [root@bcane playground]# ./helloworld.sh   
    -bash: ./helloworld.sh: Permission denied  

---
authors:
- Benjamin Cane
categories:
- Administration
- Best Practices
- How To and Tutorials
- Linux
- Linux Commands
- Security
date: '2011-09-08T20:01:06'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- tech
- unix
title: 'mount: Disabling execution of scripts'
url: /2011/09/08/mount-disabling-execution-of-scripts

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

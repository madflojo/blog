---
author: bencane
comments: true
date: 2011-08-10 20:30:06+00:00
popularity: None
slug: runlevel-check-your-current-runlevel-then-change-it
title: 'runlevel: Check your current runlevel. Then change it'
post_id: 29
categories:
- Command Line
- Linux
- Linux Commands
tags:
- init
- inittab
- linux
- runlevel
- tech
---

Today's commands are how you can check what runlevel your system is in and then change it.

**Check the current runlevel:**

    [root@bcane tmp]# runlevel   
    N 5

**Change the current runlevel:**

    [root@bcane tmp]# init <new_level>

The run levels in Unix/Linux are used to define what state init (the parent of all processes) is in. Each distribution of Unix/Linux has different definitions of what run levels starts what processes.

Usually you can find the different definitions in `/etc/inittab` below is the one from a fedora box.

    # Default runlevel. The runlevels used are:  
    # 0 - halt (Do NOT set initdefault to this)  
    # 1 - Single user mode  
    # 2 - Multiuser, without NFS (The same as 3, if you do not have networking)  
    # 3 - Full multiuser mode  
    # 4 - unused  
    # 5 - X11  
    # 6 - reboot (Do NOT set initdefault to this)




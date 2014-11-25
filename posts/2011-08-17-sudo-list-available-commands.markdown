---
author: bencane
comments: true
date: 2011-08-17 20:32:06+00:00
popularity: None
slug: sudo-list-available-commands
title: 'Sudo: List available commands'
post_id: 36
categories:
- All Articles
- Command Line
- Linux
- Linux Commands
- Unix
- Unix Commands
tags:
- linux
- sudo
- tech
- unix
---

Sudo is the Unix/Linux standard for providing users with the ability to run commands as another user. However when working with large teams sometimes its difficult to identify which user has what access, below is a command that makes it easy to see what is available for a user.

**Example:**

    [sudoguy@bcane ~]$ sudo -l  
      
    User sudoguy may run the following commands on this host:  
     (root) /bin/nice, /bin/kill, /usr/bin/kill, /usr/bin/killall, (root) /sbin/route, /sbin/ifconfig, /bin/ping, /sbin/dhclient, /usr/bin/net, /sbin/iptables, /usr/bin/rfcomm, /usr/bin/wvdial, /sbin/iwconfig, /sbin/mii-tool, (root)  
     /bin/rpm, /usr/bin/up2date, /usr/bin/yum, (root) NOPASSWD: ALL

The cool thing about this is you can also do this as root without switching to the user.

    [root@bcane ~]# sudo -lU sudoguy  
      
    User sudoguy may run the following commands on this host:  
     (ALL) NOPASSWD: ALL  
     (root) /bin/nice, /bin/kill, /usr/bin/kill, /usr/bin/killall, (root) /sbin/route, /sbin/ifconfig, /bin/ping, /sbin/dhclient, /usr/bin/net, /sbin/iptables, /usr/bin/rfcomm, /usr/bin/wvdial, /sbin/iwconfig, /sbin/mii-tool, (root)  
     /bin/rpm, /usr/bin/up2date, /usr/bin/yum, (root) NOPASSWD: ALL  
  

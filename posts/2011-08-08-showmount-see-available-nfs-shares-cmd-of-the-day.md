---
author: bencane
comments: true
date: 2011-08-08 20:00:05+00:00
popularity: None
slug: showmount-see-available-nfs-shares-cmd-of-the-day
title: 'showmount: See available NFS Shares'
post_id: 27
categories:
- Applications
- Command Line
- File Systems
- Linux
- Linux Commands
- NFS
- Unix
- Unix Commands
tags:
- bsd
- linux
- nfs
- tech
- unix
---

Showmount is a handy little command I've found out about in the recent few years. It allows you to see the available nfs shares on remote systems.

**Example:**

    $ showmount -e 192.168.0.110  
    Exports list on 192.168.0.110:  
    /volume1/music           192.168.0.1/24  
    /volume1/data            192.168.0.1/24

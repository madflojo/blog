---
authors:
- Benjamin Cane
categories:
- Applications
- Command Line
- File Systems
- Linux
- Linux Commands
- NFS
- Unix
- Unix Commands
date: '2011-08-08T20:00:05'
draft: false
header:
  caption: ''
  image: ''
tags:
- bsd
- linux
- nfs
- tech
- unix
title: 'showmount: See available NFS Shares'
url: /2011/08/08/showmount-see-available-nfs-shares-cmd-of-the-day

---

Showmount is a handy little command I've found out about in the recent few years. It allows you to see the available nfs shares on remote systems.

**Example:**

    $ showmount -e 192.168.0.110  
    Exports list on 192.168.0.110:  
    /volume1/music           192.168.0.1/24  
    /volume1/data            192.168.0.1/24

---
authors:
- Benjamin Cane
categories:
- Command Line
- Linux
- Linux Commands
date: '2011-07-22T07:51:00'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- redhat
- rpm
- tech
title: 'rpm: Finding dependencies'
url: /2011/07/22/rpm-finding-dependencies-shell-fu

---

Ever want to remove a package but needed to know what requires that package before going through dependency hell?

    # rpm -q --whatrequires kernel  
    prelink-0.3.0-13  
    tcpdump-3.7.2-7.1  
    iptables-1.2.9-1.0  
    nfs-utils-1.0.6-1

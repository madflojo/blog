---
author: bencane
comments: true
date: 2011-07-22 07:51:00+00:00
popularity: None
slug: rpm-finding-dependencies-shell-fu
title: 'rpm: Finding dependencies'
post_id: 17
categories:
- Command Line
- Linux
- Linux Commands
tags:
- linux
- redhat
- rpm
- tech
---

Ever want to remove a package but needed to know what requires that package before going through dependency hell?

    # rpm -q --whatrequires kernel  
    prelink-0.3.0-13  
    tcpdump-3.7.2-7.1  
    iptables-1.2.9-1.0  
    nfs-utils-1.0.6-1

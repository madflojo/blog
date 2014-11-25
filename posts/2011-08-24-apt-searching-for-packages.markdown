---
author: bencane
comments: true
date: 2011-08-24 20:32:05+00:00
popularity: None
slug: apt-searching-for-packages
title: 'apt: Searching for packages'
post_id: 41
categories:
- All Articles
- Command Line
- Linux
- Linux Distributions
- Ubuntu
tags:
- apt
- debian
- linux
- tech
---

Using the "Advanced Package Tool" aka **apt** to install utilities is one of the easiest ways to install software in Linux/Unix.

Here is an example of searching for packages.

**Example:**

    madflojo@eee-buntu:~/Downloads$ apt-cache search libcurl3  
    libcurl3 - Multi-protocol file transfer library (OpenSSL)  
    libcurl3-dbg - libcurl compiled with debug symbols  
    libcurl3-gnutls - Multi-protocol file transfer library (GnuTLS)  
    libcurl3-nss - Multi-protocol file transfer library (NSS)  
    libcurl4-gnutls-dev - Development files and documentation for libcurl(GnuTLS)  
    libcurl4-nss-dev - Development files and documentation for libcurl (NSS)  
    libcurl4-openssl-dev - Development files and documentation for libcurl (OpenSSL)

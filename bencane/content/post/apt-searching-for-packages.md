---
authors:
- Benjamin Cane
categories:
- All Articles
- Command Line
- Linux
- Linux Distributions
- Ubuntu
date: '2011-08-24T20:32:05'
draft: false
header:
  caption: ''
  image: ''
tags:
- apt
- debian
- linux
- tech
title: 'apt: Searching for packages'
url: /2011/08/24/apt-searching-for-packages

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

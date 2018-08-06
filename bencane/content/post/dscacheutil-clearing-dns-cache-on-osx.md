---
authors:
- Benjamin Cane
categories:
- Command Line
- OSX
- Unix
- Unix Distributions
date: '2011-10-25T20:00:00'
draft: false
header:
  caption: ''
  image: ''
tags:
- bash
- mac
- osx
- tech
title: 'dscacheutil: Clearing DNS cache on OSX'
url: /2011/10/25/dscacheutil-clearing-dns-cache-on-osx

---

This is something I ran into recently over the weekend. I made modifications to the DNS of a domain and I couldn't get my mac to recognize the change.

The culprit was DNS caching, after flushing my DNS cache all was well.

    # dscacheutil -flushcache

---
author: bencane
comments: true
date: 2011-10-25 20:00:00+00:00
popularity: None
slug: dscacheutil-clearing-dns-cache-on-osx
title: 'dscacheutil: Clearing DNS cache on OSX'
post_id: 57
categories:
- Command Line
- OSX
- Unix
- Unix Distributions
tags:
- bash
- mac
- osx
- tech
---

This is something I ran into recently over the weekend. I made modifications to the DNS of a domain and I couldn't get my mac to recognize the change.

The culprit was DNS caching, after flushing my DNS cache all was well.

    # dscacheutil -flushcache

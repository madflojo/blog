---
authors:
- Benjamin Cane
categories:
- All Articles
- Applications
- Bind
- DNS
- How To and Tutorials
date: '2011-10-06T19:32:39'
draft: false
header:
  caption: ''
  image: ''
tags:
- bind
- dns
- linkedin
- linux
- tech
- unix
title: 'bind: Checking a zone record for errors'
url: /2011/10/06/bind-checking-a-zone-record-for-errors

---

Bind is the most widely used DNS service software out there, it is the default DNS service for all of the main distributions of Unix/Linux.

While Bind is very popular it is also very tricky sometimes. One of the best ways to see if your edits are good and meet the DNS standards is to run a named-checkzone after editing a zone file and before reloading/restarting bind.

    slize:~# named-checkzone bencane.com /etc/bind/master/bencane.com.conf
    dns_master_load: /etc/bind/master/bencane.com.conf:18: bencane.com: CNAME and other data
    dns_master_load: /etc/bind/master/bencane.com.conf:18: bencane.com: CNAME and other data
    dns_master_load: /etc/bind/master/bencane.com.conf:18: bencane.com: CNAME and other data
    zone bencane.com/IN: loading from master file /etc/bind/master/bencane.com.conf failed: CNAME and other data

I got this message because of a misconfiguration around a CNAME. After correcting my zone file this is the output.

    slize:~# named-checkzone bencane.com /etc/bind/master/bencane.com.confzone bencane.com/IN: loaded serial 1130065411OK

---
authors:
- Benjamin Cane
categories:
- Command Line
- How To and Tutorials
- Solaris
- Unix
- Unix Distributions
date: '2011-08-01T03:50:00'
draft: false
header:
  caption: ''
  image: ''
tags:
- oracle
- solaris
- tech
title: 'SMF: Enable apache [Solaris]'
url: /2011/08/01/smf-enable-apache-solaris

---

As of Solaris 9, Sun introduced a new utility called Service Management Facility. This utility is now (Solaris 11) the preferred method of managing your services. While the /etc/rc.X/ directories are still around and work they are considered legacy.

Here is a quick example of enabling apache to get you started.

    # svcs -a | grep http  
    disabled 10:23:11 svc:/network/http:apache22  
    # svcadm enable http  
    # svcs -a | grep http  
    online 10:30:23 svc:/network/http:apache22

This will enable apache for not only your live session but will also enable it for boot as well.

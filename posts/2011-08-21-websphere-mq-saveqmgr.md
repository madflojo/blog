---
author: bencane
comments: true
date: 2011-08-21 13:33:06+00:00
popularity: None
slug: websphere-mq-saveqmgr
title: 'Websphere MQ: saveqmgr'
post_id: 40
categories:
- How To &amp; Tutorials
tags:
- ibm
- linux
- mq
- tech
- unix
---

If you need to export the Queue Manager configuration of MQ to a file you can do it via the saveqmgr utility.

**Syntax:**

    mqm@localhost :$ ./saveqmgr.linux -m <QMGR> -f /path/to/file.out

You can obtain this utility via IBM's website: [[http://www-01.ibm.com/support/docview.wss?uid=swg24000673](http://www-01.ibm.com/support/docview.wss?uid=swg24000673)](http://www-01.ibm.com/support/docview.wss?uid=swg24000673)

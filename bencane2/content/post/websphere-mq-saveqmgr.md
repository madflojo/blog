---
authors:
- Benjamin Cane
categories:
- How To and Tutorials
date: '2011-08-21T13:33:06'
draft: false
header:
  caption: ''
  image: ''
tags:
- ibm
- linux
- mq
- tech
- unix
title: 'Websphere MQ: saveqmgr'
url: /2011/08/21/websphere-mq-saveqmgr

---

If you need to export the Queue Manager configuration of MQ to a file you can do it via the saveqmgr utility.

**Syntax:**

    mqm@localhost :$ ./saveqmgr.linux -m <QMGR> -f /path/to/file.out

You can obtain this utility via IBM's website: [[http://www-01.ibm.com/support/docview.wss?uid=swg24000673](http://www-01.ibm.com/support/docview.wss?uid=swg24000673)](http://www-01.ibm.com/support/docview.wss?uid=swg24000673)

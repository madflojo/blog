---
author: bencane
comments: true
date: 2011-08-20 20:32:05+00:00
popularity: None
slug: sudo-running-as-a-specific-user
title: 'Sudo: Running as a specific user'
post_id: 39
categories:
- Administration
- All Articles
- Command Line
- Linux
- Linux Commands
- Security
- Unix
- Unix Commands
tags:
- linux
- sudo
- tech
- unix
---

Sudo is usually used to allow a user to run commands as root, but what happens if you want a user to run a command as another user?

You can use the example below to configure your sudo rule.

**Example:**

    [bcane@bcane ~]$ sudo -u sudoguy whoami  
    sudoguy

**The rule from /etc/sudoers:**

    bcane ALL=(sudoguy) /usr/bin/whoami, NOPASSWD: ALL

Same thing but instead of bcane the users group:

    %users ALL=(sudoguy) /usr/bin/whoami, NOPASSWD: ALL

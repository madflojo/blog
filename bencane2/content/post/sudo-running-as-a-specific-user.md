---
authors:
- Benjamin Cane
categories:
- Administration
- All Articles
- Command Line
- Linux
- Linux Commands
- Security
- Unix
- Unix Commands
date: '2011-08-20T20:32:05'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- sudo
- tech
- unix
title: 'Sudo: Running as a specific user'
url: /2011/08/20/sudo-running-as-a-specific-user

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

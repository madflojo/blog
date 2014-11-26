---
author: bencane
comments: true
date: 2011-09-01 20:01:05+00:00
popularity: None
slug: grep-counting-results
title: 'grep: Counting Results'
post_id: 46
categories:
- Command Line
- Linux
- Linux Commands
tags:
- linux
- tech
- unix
---

Grep is one of the key Unix/Linux utilities for any user, whether  you are a systems administrator, developer or general desktop user using  grep can save you a ton of time. Below is an example of counting the  number of lines that match the search string. This can be extremely  useful if you are looking through large log files or sometimes even the  passwd file.

**Example:**

    [bcane@bcane ~]$ grep -c root /etc/passwd  
    2

In  the above example you can see there are 2 lines with the word root. The  next example will show you the number of lines that do not have the  search string of root in them.

    [bcane@bcane ~]$ grep -vc root /etc/passwd  
    35

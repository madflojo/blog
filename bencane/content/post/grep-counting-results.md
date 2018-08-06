---
authors:
- Benjamin Cane
categories:
- Command Line
- Linux
- Linux Commands
date: '2011-09-01T20:01:05'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- tech
- unix
title: 'grep: Counting Results'
url: /2011/09/01/grep-counting-results

---

Grep is one of the key Unix/Linux utilities for any user, whether  you are a systems administrator, developer or general desktop user using  grep can save you a ton of time. Below is an example of counting the  number of lines that match the search string. This can be extremely  useful if you are looking through large log files or sometimes even the  passwd file.

**Example:**

    [bcane@bcane ~]$ grep -c root /etc/passwd  
    2

In  the above example you can see there are 2 lines with the word root. The  next example will show you the number of lines that do not have the  search string of root in them.

    [bcane@bcane ~]$ grep -vc root /etc/passwd  
    35

---
authors:
- Benjamin Cane
categories:
- All Articles
- Command Line
- Linux
- Linux Commands
- Unix
- Unix Commands
date: '2011-08-19T20:32:06'
draft: false
header:
  caption: ''
  image: ''
tags:
- find
- linux
- tech
- unix
title: Find broken Links
url: /2011/08/19/find-broken-links

---

At the end of the day this is easier than I expected.

**Example:**

    [root@bcane play]# find ./ -follow -lname "*"  
    ./somedir4  
    ./somedir7  
    ./somedir6  
    ./somedir5  
    [root@bcane play]# ls -la  
    total 12  
    drwxrwxr-x. 3 bcane bcane 4096 Aug 15 18:35 .  
    drwxrwxrwt. 4 root root 4096 Aug 15 18:28 ..  
    drwxr-xr-x. 2 bcane root 4096 Aug 15 18:42 somedir  
    lrwxrwxrwx. 1 root root 7 Aug 15 18:35 somedir1 -> somedir  
    lrwxrwxrwx. 1 root root 7 Aug 15 18:35 somedir2 -> somedir  
    lrwxrwxrwx. 1 root root 7 Aug 15 18:35 somedir3 -> somedir  
    lrwxrwxrwx. 1 root root 10 Aug 15 18:35 somedir4 -> somedir_no  
    lrwxrwxrwx. 1 root root 10 Aug 15 18:35 somedir5 -> somedir_no  
    lrwxrwxrwx. 1 root root 10 Aug 15 18:35 somedir6 -> somedir_no  
    lrwxrwxrwx. 1 root root 10 Aug 15 18:35 somedir7 -> somedir_no

Once you've found the broken links you can delete them easily.

    [root@bcane play]# find ./ -follow -lname "*" -delete  
    [root@bcane play]# ls -la  
    total 12  
    drwxrwxr-x. 3 bcane bcane 4096 Aug 15 18:43 .  
    drwxrwxrwt. 4 root root 4096 Aug 15 18:28 ..  
    drwxr-xr-x. 2 bcane root 4096 Aug 15 18:42 somedir  
    lrwxrwxrwx. 1 root root 7 Aug 15 18:35 somedir1 -> somedir  
    lrwxrwxrwx. 1 root root 7 Aug 15 18:35 somedir2 -> somedir  
    lrwxrwxrwx. 1 root root 7 Aug 15 18:35 somedir3 -> somedir

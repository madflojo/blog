---
authors:
- Benjamin Cane
categories:
- Command Line
- Linux
- Linux Commands
- Unix
- Unix Commands
date: '2011-07-14T23:02:06'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- tech
- unix
title: 'Tar: Don''t touch existing files'
url: /2011/07/14/tar-dont-touch-existing-files-shell-fu

---

Tar is a handy dandy command, Its function is to create and extract archive files known as tarfiles. While tar can be used in various situations, one situation is when you need to move files from one server to another while maintaining permissions. Tar will retain the permissions and allow you to transfer 1 big file rather than many files.

In this situation there could be a time where you don't want tar to overwrite files that already exist. Well tar can take care of that as well by adding the `-k` flag.

**Example:**

    [bcane@bcane play]$ echo 1 > 1.txt   
    [bcane@bcane play]$ tar -xzf files.tgz 1.txt  
    [bcane@bcane play]$ cat 1.txt   
    [bcane@bcane play]$ echo 1 > 1.txt   
    [bcane@bcane play]$ tar -xzf files.tgz 1.txt -k  
    [bcane@bcane play]$ cat 1.txt   
    1

Also note the placement of the `-k` matters, if it is mixed with the `-xzf` it will not work.

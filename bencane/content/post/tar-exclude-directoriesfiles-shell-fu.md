---
authors:
- Benjamin Cane
categories:
- Command Line
- Linux
- Linux Commands
- Unix
- Unix Commands
date: '2011-07-26T08:00:32'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- tech
- unix
title: 'tar: Exclude directories/files'
url: /2011/07/26/tar-exclude-directoriesfiles-shell-fu

---

Tar is a essential commands for a Linux/Unix user, when it comes to archiving or copying files tar is my favorite.

Today's shell-fu examples will show you how to create a tar file that excludes specified directories and files. You can achieve this two ways.

## 1. Using the --exclude flag

    [bcane@bcane play]$ tar -cvzf ../tar.tgz --exclude="./somedir" ./  
    ./  
    ./files.tgz  
    ./list.txt  
    ./3.txt  
    ./2.txt  
    ./4.txt  
    ./1.txt

## 2. Using the -X flag followed by a file to read

    [bcane@bcane play]$ cat list.txt   
    1.txt  
    2.txt  
    3.txt  
    [bcane@bcane play]$ tar -cvzf ../tar.tgz -X list.txt ./  
    ./  
    ./files.tgz  
    ./list.txt  
    ./somedir/  
    ./4.txt

The second option is very handy when you have a large list of files/directories to exclude.

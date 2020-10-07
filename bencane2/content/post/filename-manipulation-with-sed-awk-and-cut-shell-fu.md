---
authors:
- Benjamin Cane
categories:
- Command Line
- Linux Commands
- Shell Scripting
- Unix Commands
date: '2011-08-05T06:27:48'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- osx
- tech
- unix
title: Filename manipulation with sed, awk and cut
url: /2011/08/05/filename-manipulation-with-sed-awk-and-cut-shell-fu

---

Working with files is one of the most common tasks for systems administrators; because of that there are numerous ways to work with files in the Linux/Unix environment.

Here is 2 quick examples on how to rename files.

**Example:**

    imadmac:testing madflojo$ ls -la  
    total 32  
    drwxr-xr-x 6 madflojo wheel 204 Aug 4 20:11 .  
    drwxrwxrwt 6 root   wheel 204 Aug 4 20:10 ..  
    -rw-r--r-- 1 madflojo wheel  8 Aug 4 20:11 1.txt  
    -rw-r--r-- 1 madflojo wheel  8 Aug 4 20:11 2.txt  
    -rw-r--r-- 1 madflojo wheel  8 Aug 4 20:11 3.txt  
    -rw-r--r-- 1 madflojo wheel  8 Aug 4 20:11 4.txt

Today we are going to change these .txt files to a .file extension.

    imadmac:testing madflojo$ for x in `ls | cut -d. -f1`  
    do  
    mv $x.txt $x.file  
    done  
    imadmac:testing madflojo$ ls -la  
    total 32  
    drwxr-xr-x 6 madflojo wheel 204 Aug 4 20:15 .  
    drwxrwxrwt 6 root   wheel 204 Aug 4 20:10 ..  
    -rw-r--r-- 1 madflojo wheel  8 Aug 4 20:11 1.file  
    -rw-r--r-- 1 madflojo wheel  8 Aug 4 20:11 2.file  
    -rw-r--r-- 1 madflojo wheel  8 Aug 4 20:11 3.file  
    -rw-r--r-- 1 madflojo wheel  8 Aug 4 20:11 4.file

In the above example we are simply getting a list of files but removing the .txt, from there we run a for loop that moves the variable $x.txt to $x.file.

We will do the same thing but this time with sed  

    imadmac:testing madflojo$ for x in `ls | sed -e 's/.txt$//'`  
    do  
    mv $x.txt $x.file  
    done  
    imadmac:testing madflojo$ ls -la  
    total 32  
    drwxr-xr-x 6 madflojo wheel 204 Aug 4 20:21 .  
    drwxrwxrwt 6 root   wheel 204 Aug 4 20:10 ..  
    -rw-r--r-- 1 madflojo wheel  8 Aug 4 20:11 1.file  
    -rw-r--r-- 1 madflojo wheel  8 Aug 4 20:11 2.file  
    -rw-r--r-- 1 madflojo wheel  8 Aug 4 20:11 3.file  
    -rw-r--r-- 1 madflojo wheel  8 Aug 4 20:11 4.file
  
Now with awk  

    imadmac:testing madflojo$ for x in `ls | awk -F. '{print $1}'`  
    do  
    mv $x.txt $x.file  
    done  
    imadmac:testing madflojo$ ls -la  
    total 32  
    drwxr-xr-x 6 madflojo wheel 204 Aug 4 20:23 .  
    drwxrwxrwt 6 root   wheel 204 Aug 4 20:10 ..  
    -rw-r--r-- 1 madflojo wheel  8 Aug 4 20:11 1.file  
    -rw-r--r-- 1 madflojo wheel  8 Aug 4 20:11 2.file  
    -rw-r--r-- 1 madflojo wheel  8 Aug 4 20:11 3.file  
    -rw-r--r-- 1 madflojo wheel  8 Aug 4 20:11 4.file  

There are many cool things you can do with sed, awk, and cut but this should get you started with some useful applications.

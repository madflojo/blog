---
authors:
- Benjamin Cane
categories:
- All Articles
- Command Line
- Programming
- Shell Scripting
date: '2011-08-04T00:41:00'
draft: false
header:
  caption: ''
  image: ''
tags:
- bash
- linux
- tech
- unix
title: 'Bash: Repeated tasks with seq and for loops'
url: /2011/08/04/bash-repeated-tasks-with-seq-and-for-loops-shell-fu

---

There comes a time where every sysadmin needs to execute the same task multiple times. Whether you need to create 12,000 2MB files, create multiple users, or simply delete more then 50k files at a time; for loops will save you time and typing.

For the instances where you need to execute a for loop a specific amount of times you can use seq to your advantage.

Today's example will show you how to create multiple files.

**Example:**

    bcane@fedora:~$ for x in `seq 1 1 10`; do touch test.$x.txt; done  
    bcane@fedora:~$ ls -la test.*  
    -rw-r--r-- 1 bcane bcane 0 2011-08-03 14:31 test.10.txt  
    -rw-r--r-- 1 bcane bcane 0 2011-08-03 14:31 test.1.txt  
    -rw-r--r-- 1 bcane bcane 0 2011-08-03 14:31 test.2.txt  
    -rw-r--r-- 1 bcane bcane 0 2011-08-03 14:31 test.3.txt  
    -rw-r--r-- 1 bcane bcane 0 2011-08-03 14:31 test.4.txt  
    -rw-r--r-- 1 bcane bcane 0 2011-08-03 14:31 test.5.txt  
    -rw-r--r-- 1 bcane bcane 0 2011-08-03 14:31 test.6.txt  
    -rw-r--r-- 1 bcane bcane 0 2011-08-03 14:31 test.7.txt  
    -rw-r--r-- 1 bcane bcane 0 2011-08-03 14:31 test.8.txt  
    -rw-r--r-- 1 bcane bcane 0 2011-08-03 14:31 test.9.txt  

## Why it works

The command seq will output numbers based on the criteria you give it. The first number you provide seq is the number you want to start with, the second is the number you want to increment by. For example if you put seq 1 2 10 you would get an output of 1, 3, 5, 7, & 9. The last number in the list is the number you want to end with, as you can see from my 1 2 10 example if 10 is not the last number in the increment it will stop on the number before.

    bcane@fedora:~$ seq 1 2 10  
    1  
    3  
    5  
    7  
    9  
    bcane@fedora:~$ seq 1 1 10  
    1  
    2  
    3  
    4  
    5  
    6  
    7  
    8  
    9

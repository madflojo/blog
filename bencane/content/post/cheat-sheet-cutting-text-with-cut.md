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
date: '2012-10-22T16:30:01'
draft: false
header:
  caption: ''
  image: ''
tags:
- all
- awk
- bash
- csv file
- cut
- gnu linux
- linux
- ubuntu
- unix
title: 'Cheat Sheet: Cutting Text with cut'
url: /2012/10/22/cheat-sheet-cutting-text-with-cut

---

The cut command is a Unix/Linux tool used to literally cut text from files and output from other commands. With the cut command a user can take text and output only certain parts of the line.

In my opinion cut is the most under recognized and utilized command in Linux/Unix. This is mostly due to the fact that when most Sysadmins want to cut text from files or standard output many will reach for AWK.

While AWK is a great tool for quick and dirty commands; I tend to reach for cut before AWK. The below cheat sheet should show many ways to use cut with every day tasks.

### Common Separated Values

#### Print the first field out of a CSV file
     
     $ cut -d: -f1 passwd.bak 
       root
       daemon

#### Print the first field out of CSV output from another command
     
     $ head -1 /etc/passwd | cut -d: -f1 
       root

#### Print the first, second, and seventh field out of a CSV file

To change the field simply change the numbers after `-f` separated by a comma.
     
     $ cut -d: -f1,2,7 passwd.bak 
      root:x:/bin/bash

#### Print text based on Spaces
     
     $ cut -d  -f3 /etc/motd 
      Ubuntu

#### Print the fourth field and everything after that from a command

This command is pretty handy if you wanted to make a script out of the past few commands you ran.
     
     $ history | cut -d  -f 4- 
      ping google.com

#### Print up to the 4th field
     
     $ cut -d  -f-4 /etc/motd 
      Welcome to Ubuntu 12.04

#### Print all fields between 5 and 8
     
     $ cut -d: -f5-8 passwd 
      root:/root:/bin/bash

#### Output with a different delimiter (make a CSV)

##### Convert : to ,
     
     $ cut --output-delimiter=, -d: -f1- passwd 
      root,x,0,0,root,/root,/bin/bash

##### Convert space to ,
     
     $ ps -elf | cut --output-delimiter=, -d -f1-
     F,S,UID,,,,,,,,PID,,PPID,,C,PRI,,NI,ADDR,SZ,WCHAN,,STIME,TTY,,,,,,,,,,TIME,CMD
     4,S,root,,,,,,,,,1,,,,,0,,0,,80,,,0,-,,6083,poll_s,19:07,?,,,,,,,,00:00:12,/sbin/init

#### Output only lines that have a delimiter

This command will only output lines that have a : (in our example), within the file tmpfile there are multiple lines some with : and some without.
     
     $ head tmpfile
     Welcome to Ubuntu 12.04 LTS (GNU/Linux 3.2.0-29-generic x86_64)
     73 packages can be updated.
     10 updates are security updates.
     root:x:0:0:root:/root:/bin/bash
     daemon:x:1:1:daemon:/usr/sbin:/bin/sh
     bin:x:2:2:bin:/bin:/bin/sh
     sys:x:3:3:sys:/dev:/bin/sh
     sync:x:4:65534:sync:/bin:/bin/sync

     $ cut -s -d: -f1-4 tmpfile
     root:x:0:0
     daemon:x:1:1
     bin:x:2:2
     sys:x:3:3
     sync:x:4:65534

### Bytes

#### Print bytes 1 through 45
     
     $ cut -b1-45 /etc/motd
     Welcome to Ubuntu 12.04 LTS (GNU/Linux 3.2.0-

#### Print everything but bytes 10 through 45
     
     $ cut --complement -b10-45 /etc/motd
     Welcome t29-generic x86_64)

### Characters

#### Print characters 1 through 25
     
     $ cut -c1-25 /etc/motd
     Welcome to Ubuntu 12.04 L

#### Print everything but characters 10 through 25
     
     $ cut --complement -c10-25 /etc/motd
     Welcome tTS (GNU/Linux 3.2.0-29-generic x86_64)

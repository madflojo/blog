---
authors:
- Benjamin Cane
categories:
- Command Line
- Linux
- Linux Commands
- Unix
- Unix Commands
date: '2011-08-06T02:20:00'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- tech
- unix
title: Counting with sort and uniq
url: /2011/08/06/counting-with-sort-and-uniq-shell-fu

---

Here is another quick example of how to get a count of how many times a string appears. For my example I am going to use this output.

    $ cat /etc/passwd | cut -d: -f7
    /bin/bash
    /bin/sh
    /bin/sh
    /bin/sh
    /bin/sync
    /bin/sh
    /bin/sh
    /bin/sh

These are the shells of users on my system, what if I wanted to see what the most common shell was?

    $ cat /etc/passwd | cut -d: -f7 | sort | uniq -c | sort -nk1
    1 /bin/sync
    2 /usr/sbin/nologin
    4 /bin/false
    5 /bin/bash
    20 /bin/sh

In order to get this result I take my output and send it to sort, this command will sort the output alphabetically. From there we pipe it to uniq -c which will find all of the unique occurrences of a string and print the number of times it shows up. We then sort by that number and BAM, we have a list of shells and how many users are using them.

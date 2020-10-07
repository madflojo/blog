---
authors:
- Benjamin Cane
categories:
- Administration
- All Articles
- Best Practices
- Command Line
- Linux
- Linux Commands
- Unix
- Unix Commands
date: '2011-07-22T08:21:00'
draft: false
header:
  caption: ''
  image: ''
tags:
- apple
- linux
- max osx
- osx
- tech
- unix
title: Truncating a large log file
url: /2011/07/22/truncating-a-large-log-file-best-practices

---

This is actually one of my favorite questions to ask Jr. Systems Administrators. I believe the way they answer this question really helps me gauge where they are at in their Administration skills.

How do you clear a large log file that an application is actively writing to?

Some will answer honestly and say "by removing the file" and others will pretend like they careful of everything and say "move the file out of the way and create a new one".

The correct answer is "truncate the file using the redirect symbol" or if you really want to pretend like you are super careful "make a copy of the file then truncate it using the redirect symbol"

**Example:**

    # > /tmp/big.log

One thing most will neglect to tell me is why do they truncate the file rather than simply using the move command?

Well the answer is because of open file handles, if a running process has an open file handle on the log file in question when you perform the mv command the file handle will follow the file to the new location. If that happens all of the new data will be written to the new location rather than the correct location.

**Example:**

    # fuser /tmp/big.log  
    /tmp/big.log: 2246  
    # mv /tmp/big.log /tmp/big.log2  
    # fuser /tmp/big.log2 
    /tmp/big.log2: 2246

This can mean misplaced log data which could be a very big headache for you later. Especially if you had monitoring software reading /tmp/big.log periodically.  
If you use the redirect symbol to truncate the file than you will empty the contents of the file without disrupting any existing open file handles.  
  
**Example:**

    # fuser /tmp/big.log2  
    /tmp/big.log2: 2246  
    # > /tmp/big.log2 
    # fuser /tmp/big.log2  
    /tmp/big.log2: 2246

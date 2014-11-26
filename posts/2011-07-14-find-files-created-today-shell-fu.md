---
author: bencane
comments: true
date: 2011-07-14 02:54:48+00:00
popularity: None
slug: find-files-created-today-shell-fu
title: Find files created today
post_id: 13
categories:
- Command Line
- Linux
- Linux Commands
- Unix
- Unix Commands
tags:
- linux
- shell
- tech
- unix
---

I figured I would start a new category for command line quickies. Here is one that I have found very useful.

    # find ./ -type f -daystart -ctime -1

This is a very nice way of finding files created today. Now this command differs from the command below.

    # find ./ -type f -ctime -1

The `-daystart` flag will tell find to use the beginning of the day when searching for files created today. Without daystart the `ctime -1` flag will tell find to find files created in the last 24 hours.

---
author: bencane
comments: true
date: 2011-07-01 23:11:38+00:00
popularity: None
slug: bash-random
title: Bash $RANDOM
post_id: 5
categories:
- How To &amp; Tutorials
- Linux Commands
- Shell Scripting
- Unix Commands
tags:
- bash
- linux
- unix
---

Found this cool little thing today when I was looking for a way to create a random number in BASH. It seems that BASH does the hard work for you and creates a variable called $RANDOM

    # echo $RANDOM  
    26031  
    # echo $RANDOM  
    20163  
    # echo $RANDOM  
    30045

And if you want to print off a certain range such as 0 - 100 you can do it like so.

    # echo $((RANDOM%100))  
    81

Figured I would share this as it is a cool little trick.

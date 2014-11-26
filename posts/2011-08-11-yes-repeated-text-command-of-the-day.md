---
author: bencane
comments: true
date: 2011-08-11 20:33:06+00:00
popularity: None
slug: yes-repeated-text-command-of-the-day
title: 'yes: Repeated Text'
post_id: 30
categories:
- All Articles
- Command Line
- Linux
- Linux Commands
- Unix
- Unix Commands
tags:
- linux
- tech
- unix
---

Ever feel like you are repeating yourself? Well with yes you can type a string only once and it will repeat; over and over and over and over and over again.

**Example:**

    [bcane@bcane tmp]$ yes "yes will print repeated text"   
    yes will print repeated text  
    yes will print repeated text  
    yes will print repeated text  
    yes will print repeated text  
    yes will print repeated text

So why would you want a command that prints text repeatedly? Ever run into situations like this?

    [bcane@bcane somedir]$ rm -i *.txt  
    rm: remove regular empty file `100.txt'? y  
    rm: remove regular empty file `10.txt'?
    
While rm has a -f flag that will not ask you if you want to remove the file there are other commands/scripts that do not.
    
    [bcane@bcane somedir]$ ls | wc -l  
    100  
    [bcane@bcane somedir]$ yes y | rm -i *.txt  
    **Output Truncated**  
    [bcane@bcane somedir]$ ls | wc -l  
    0

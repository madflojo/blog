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
date: '2011-08-11T20:33:06'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- tech
- unix
title: 'yes: Repeated Text'
url: /2011/08/11/yes-repeated-text-command-of-the-day

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

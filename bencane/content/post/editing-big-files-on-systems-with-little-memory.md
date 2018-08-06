---
authors:
- Benjamin Cane
categories:
- Administration
- Best Practices
- Linux Commands
- Unix Commands
date: '2011-07-09T06:08:00'
draft: false
header:
  caption: ''
  image: ''
tags:
- apple
- bsd
- linux
- mac
- os x
- osx
- tech
- unix
title: Editing big files on systems with little memory
url: /2011/07/09/editing-big-files-on-systems-with-little-memory

---

A friend of mine had a question on how to edit a huge (like as in xbox hueg) file without using vi. He probably didn't want to use vi because when you vi a file it will load the entire file into memory. This can be very bad if your system doesn't have enough memory to accommodate the file size.

So how do you edit a specific line of a file without loading it into memory? It's simple using head and tail.

Using head you can specify the line numbers to grab from the top of a file. Tail is the exact opposite but it also has a cool option that allows it to grab every line after the specified line number (using the +).

I did the following on my OS X machine; after all its a Unix machine as well.

    # cat original.file  
    1  
    2  
    3  
    4  
    5  
    6  
    7  
    8  
    9  
    10  
  
    # head -n 4 original.file  new.file  
    # echo "5 is new"  new.file  
    # tail -n +6 original.file  new.file  
    # cat new.file  
    1  
    2  
    3  
    4  
    5 is new  
    6  
    7  
    8  
    9  
    10  

From my testing tail will not load an entire file into memory. I Tested this on OS X and Debian.

---
authors:
- Benjamin Cane
categories:
- All Articles
- How To and Tutorials
- Programming
- Shell Scripting
date: '2011-09-20T20:01:05'
draft: false
header:
  caption: ''
  image: ''
tags:
- bash
- linux
- tech
- unix
title: 'bash: Field Separator Variable'
url: /2011/09/20/bash-field-separator-variable

---

By default when using a for loop in bash the field separator is set to a space.

Example:

    [bcane@bcane ~]$ for x in list:like:this; do echo $x; done  
    list:like:this

One of the cool things about bash is that you can change this by setting a simple variable $IFS

    [bcane@bcane ~]$ IFS=":"  
    [bcane@bcane ~]$ for x in list:like:this; do echo $x; done  
    list like this

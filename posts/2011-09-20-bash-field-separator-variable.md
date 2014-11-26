---
author: bencane
comments: true
date: 2011-09-20 20:01:05+00:00
popularity: None
slug: bash-field-separator-variable
title: 'bash: Field Separator Variable'
post_id: 51
categories:
- All Articles
- How To &amp; Tutorials
- Programming
- Shell Scripting
tags:
- bash
- linux
- tech
- unix
---

By default when using a for loop in bash the field separator is set to a space.

Example:

    [bcane@bcane ~]$ for x in list:like:this; do echo $x; done  
    list:like:this

One of the cool things about bash is that you can change this by setting a simple variable $IFS

    [bcane@bcane ~]$ IFS=":"  
    [bcane@bcane ~]$ for x in list:like:this; do echo $x; done  
    list like this

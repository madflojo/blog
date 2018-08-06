---
authors:
- Benjamin Cane
categories:
- Linux Basics
- Shell
date: '2014-03-05T08:30:00'
description: An overview of the Linux directory structure and how to move around it
  with the cd command.
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- redhat
- centos
- bash
- linux shell
- unix shell
- linux directory structure
- linux directories
- linux cd
- linux pwd
title: Getting around the Linux directory structure with the cd command
url: /2014/03/05/getting-around-the-linux-directory-structure-with-the-cd-command

---

Today is very much a "back to the basics" kind of day. In this article I am going to cover one of the most basic commands in Linux; the `cd` command. While today's article might be basic; it is always good even for experienced sysadmins, to look back at some of the basics and see if there are ways to improve your command line skills and Linux knowledge.

## The Linux/Unix directory structure

Before getting into how to change to another directory, let's take a minute to cover how Linux's directory structure is laid out. Linux's directory structure is a hierarchical directory structure, what this means is that there is a top-level or **root** directory and there are multiple levels of directories within the **root** directory. Most common Linux & Unix file systems support directories existing within other directories allowing for quite an extensive multi-level directory structure.

In Linux/Unix the root directory is symbolized by a `/` character. Any directories within the root directory can be targeted by putting `/` in front of the directories name, if we were to target the `etc` directory we could do so by referencing `/etc`. In addition to symbolizing the root directory the `/` character is also used to separate directories when referencing absolute paths. To continue with our `etc` example if we wanted to target the `network` directory inside of `etc` we could do so by referencing `/etc/network`.

## The cd command

When logging into a Linux shell either remotely through SSH or locally through a terminal/console, usually you will find yourself in a users home directory. While in general you can accomplish many things from this directory alone, you may find that at some point you want to move to another directory. To accomplish this we can use the `cd` command, this command will change the shell processes **current working directory** to the directory specified.

**Syntax**

    $ cd /path/to/directory

The below example will show how to use the `cd` command to change to the `/etc/network` directory.

**Example**

    $ cd /etc/network


## Full Paths vs Relative Paths

The example path of `/etc/network` is what is referred to as a **Full Path** or **Absolute Path**. This method of referencing a directory or file is helpful to know as it allows you to target the `network` directory no matter what your current working directory is. 

The alternative to referencing a directory via an **Absolute Path** is by referencing it with a **Relative Path**. A relative path is used when you reference a path based on your current working directory. For example if you were in the `etc` or `/etc` directory and you wanted to target the `network` directory you could by simply specify `network`. While this may be a little complicated to understand at first, the examples below should help clarify the difference between an absolute path and relative path.

## Using the cd command

### Specifying a relative path

Specifying a relative path is useful for targeting a directory that is within or near your current directory. As an example, let's say you are currently in the `/home/reader` directory and you wanted to change into `/home/reader/blog` you could specify the full `/home/reader/blog` path or you can save yourself typing and just specify `blog`.

    $ pwd
    /home/reader
    $ cd blog
    $ pwd
    /home/reader/blog

In the above example I used the `pwd` or **Print Working Directory** to print my current directory, this command is pretty helpful for finding out where you are.

### Specifying an absolute path

An absolute path is helpful for referencing a directory that is not near your current directory. For example, if you were located in `/home/reader/some/other/directory` and you wanted to go to `/etc` it is far easier to reference it as `/etc` rather than trying to use a relative path.

    $ pwd
    /home/reader/some/other/directory
    $ cd /etc
    $ pwd
    /etc

In addition to the example above it is generally best to use absolute paths within scripts. Users tend to run scripts from any directory and by using absolute paths you ensure that you will be able to find any files/directories the script requires, even if it was called from an unexpected directory. 

### Going back a directory

In Unix & Linux shells the `.` character symbolizes the current directory; Two of these characters `..` represent the directory above the current directory. You can use `..` to change to another higher level directory very quickly. This is a relative path that can reference directories above the current working directory.

    $ pwd
    /home/reader/blog
    $ cd ..
    $ pwd
    /home/reader

You can also string multiple `..` characters together separated by a `/` to navigate up multiple directories.

    $ pwd
    /home/reader/blog
    $ cd ../../../
    $ pwd
    /

The `..` can also be used with directory names to navigate up one directory and then down other sub-directories.

    $ pwd
    /home/reader/blog
    $ cd ../example
    $ pwd
    /home/reader/example

### A few cd tricks

The above commands are all you really need to know to get around the Linux file system, however the below commands are some quick tricks that will help navigate the Linux file system faster.

#### Change to your home directory

The quickest way to change back to your home directory is to simply type `cd` with no arguments.

    $ pwd
    /var/tmp
    $ cd
    $ pwd
    /home/madflojo

While not providing arguments is the quickest (in terms of characters typed) another method is to specify `~` which stands for your users home directory.

    $ pwd
    /var/tmp
    $ cd ~
    $ pwd
    /home/madflojo

#### Change to another users home directory

The `~` can be used to specify another users directory as well, for example if you wanted to switch to the **test** users directory you can do so by specifying `~test`.

    $ pwd
    /var/tmp
    $ cd ~test
    $ pwd
    /home/test

## Additional Reading

The directory structure in Linux and most modern day Unix distributions follow the [Filesystem Hierarchy Standard](http://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard) which outlines a recommended structure for common files like configuration files and binaries. If you wanted to learn about how Linux and Unix organize their file systems I suggest looking at the [Filesystem Hierarchy Standard](http://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard). 

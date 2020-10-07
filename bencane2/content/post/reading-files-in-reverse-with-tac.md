---
authors:
- Benjamin Cane
categories:
- All Articles
- Command Line
- Linux
- Linux Commands
- Shell Scripting
- SysAdmin Basics
date: '2013-08-26T06:00:40'
description: A cool trick that shows how to read files in reverse with the tac command
draft: false
header:
  caption: ''
  image: ''
tags:
- bash
- cat
- gnu linux
- linux
- linux os
- red hat os
- scripting
- shell commands
- sort
- tac
title: Reading files in reverse with tac
url: /2013/08/26/reading-files-in-reverse-with-tac

---

Today's article is going to cover a command that falls into the **"I don't use this often, but when I do it's awesome"** category.

The `tac` command is very similar to the `cat` command in that it is used to concatenate and print files. However there is one very large difference, the `tac` command does this in reverse, starting with the last line of the file and working its way up to the first line.

## Using tac

#### Reading a file normally with cat

    $ cat sample.txt 
    This is line 1
    This is line 2
    This is line 3
    This is line 4
    This is line 5

#### Reading a file in reverse with tac

    $ tac sample.txt 
    This is line 5
    This is line 4
    This is line 3
    This is line 2
    This is line 1

#### Printing standard input in reverse with tac

    $ grep "line [3-5]" sample.txt | tac
    This is line 5
    This is line 4
    This is line 3

## When would you use tac?

To be frank, I've only used tac on a hand full of occasions. Most of the times where I used `tac` I later found out there was another way to get the same results. Either way here is a list of scenarios that I came up with where `tac` could be useful.

#### If someone removed the tail binary...

    $ tac sample.txt | head -n 2 | tac
    This is line 4
    This is line 5

#### Iterating through a for loops input backwards

    $ for x in `find ./ -type d | tac`; do echo $x; done
    ./directory2/1
    ./directory2/91
    ./directory2/81
    ./directory2/

Got any other use cases? Throw them in the comments, I would love to hear how folks have used `tac` in their daily lives.

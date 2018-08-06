---
authors:
- Benjamin Cane
categories:
- All Articles
- Command Line
- Linux
- Linux Commands
- Programming
- Shell Scripting
- SysAdmin Basics
- Unix
- Unix Commands
date: '2013-08-19T08:00:43'
description: A lot of sysadmins don't realize you can use grep without cat, this article
  should settle that. It also shows some other grep tricks.
draft: false
header:
  caption: ''
  image: ''
tags:
- bash
- grep
- grep -v
- linux
- linux os
- red hat os
- shell best practices
- shell scripting
title: Grepping a file without using cat, and other grep tricks
url: /2013/08/19/grepping-a-file-without-using-cat-and-grep-other-tricks

---

The grep command is a command that most Linux users learn early on, and many times they learn to use it via pipes (stdin). Because of this some Linux users just assume that grep can only be used with stdin; it's ok, I was one of those too!

Before I continue with some grep tricks I want to clarify the basic grep usage.

**Stop Doing This:**

    $ cat file.log | grep "something"
     something

**Do This More:**

    $ grep "something" file.log
     something

Aside from saving yourself some typing, this method is preferred because you only have to read and search the file through one process. The previous method requires both the `cat` and `grep` command to run; which takes longer to run and uses more system resources (even if they are minor resources, it's less efficient).

## Grep Command Tricks

The grep command is a powerful search tool, below are some examples of grep commands that I have found incredibly useful in daily tasks.

### Show Everything Except the Search Term

Normally grep will return the string that you are searching for, when given the `-v` flag grep will omit the searched string and return everything else.

    $ grep -v "something" file.log 
    this
    that
    or
    other

While I've used `-v` with grep in many use cases one that pops up is performing multiple rm commands through a for loop or xargs.

    $ ls | grep -v ".log" | xargs rm

The above command will remove all files in the current directory except the ones with .log in their filename.

### Counting the number of occurrences

One of my most common usages of grep is counting the number of times a search string is found. This is accomplished with the `-c` flag. I use this frequently when writing bash scripts to check if something is true or false.

    $ grep -c "something" file.log
    1

### Searching Multiple Files

Sometimes, when you need to search for "something" you need to search multiple files, this is as simple as giving grep multiple files to search.

    $ grep "something" ./*
     ./1:something
     ./10:something
     ./10.log:something
     ./1.log:something

### Searching through multiple files recursively

If you need to search through multiple files like the above example, but the files are in separate directories. There is no need for complicated find commands. The grep command can be used recursively as well. Though this feature isn't available on older implementations of grep, most up to date systems will have this feature.

    $ grep -r something ./*
    ./greppage/7.log:something
    ./greppage/1.log:something
    ./greppage/9.log:something
    ./greppage/8.log:something

### Finding Only the Filenames

If you want to find a string in multiple files, but only want to know the filenames of those files (to run in a for loop maybe?). The `-l` flag will accomplish this without needing to call any awk or cut commands.

    $ grep -l "something" ./*
     ./1
     ./10
     ./10.log
     ./1.log

### Finding filenames that don't contain the search term

Much like the `-v` flag, the `-L` flag is the opposite of `-l`. Rather than returning filenames of files that contain the string, this option will return filenames of files that do not contain the search string.

    $ grep -L "something" ./*
     ./20.log

### Searching with case in-sensitivity

This command is useful for those items that may or may not be capitalized.

    $ grep "something" 21.log
    $ grep -i "something" 21.log
     SOMETHING

### Outputting only the specified search term on a given line

By default with grep when you search for a string it will return the entire line that the string is on. While this is useful in some cases, sometimes you just want to see the specific search term. The `-o` flag may save you some awk or cut commands here and there in the future.

    $ grep "something" 22.log
     this that or something else
    $ grep -o "something" 22.log
     something

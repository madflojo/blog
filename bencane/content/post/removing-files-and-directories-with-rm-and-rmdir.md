---
authors:
- Benjamin Cane
categories:
- Cheat Sheets
- Command Line
- Linux
- Linux Commands
- SysAdmin Basics
- Unix
- Unix Commands
date: '2013-05-13T04:16:25'
description: A simple guide on using rm and rmdir some of the basic Shell commands
  in Linux and Unix environments
draft: false
header:
  caption: ''
  image: ''
tags:
- bash
- empty directories
- linux
- rm command
- rmdir command
- sysadmin
- unix
- learn linux
title: Removing Files and Directories with rm and rmdir
url: /2013/05/13/removing-files-and-directories-with-rm-and-rmdir

---

Normally on this blog I tend to write about more complicated tasks or fancy Linux tricks and completely overlook some of the most basic tasks that a SysAdmin needs to know. Today I have decided that I will make my blog a little more comprehensive and add some posts with some of the basics.

Along with this I will be starting a new category, called Sysadmin Basics and I will try to post an additional article each week that covers some of the more basic concepts and commands used by Linux and Unix Sysadmins.

## Remove Directories with the rmdir command

The rmdir command is used to delete and remove **empty** directories. I bolded empty as it is important to note that rmdir will only remove a directory if there are no files within that directory. If you want to remove a directory and all files within that directory, skip down to the rm section of this article.

#### Remove a single empty directory

    # rmdir somedir/

#### Remove multiple empty directories (in a single tree)

    # rmdir -p somedir/a/b/c/d/e/f/whoa

While rmdir will not remove directories with files in it; rmdir will recursively remove a directory tree that has no files. In the example somedir only has directory a within it, and the a directory only has b which only has c and so on.

#### Remove multiple empty directories

The above command will also fail if there are multiple directories in one single directory, to handle that scenario you can list the directories individually and include the `--ignore-fail-on-non-empty` flag.

    # rmdir --ignore-fail-on-non-empty -p somedir/a/b/c/ somedir/a2/b2/

Without the `--ignore-fail-on-non-empty` flag the command will still print that somedir is not empty even though it removes somedir. This is due to the fact that both command line arguments ask rmdir to remove somedir and rmdir cannot remove that directory until the last step.

## Removing Files and Directories with the rm Command

While the rmdir command is solely for directories the rm command can remove both files and directories. With the right combination of flags rm will also remove entire directories, files and all.

#### Remove a file

    # rm a-file
     rm: remove regular empty file `a-file'? y

On it's own rm will not prompt a user before removing a file; to keep systems safe from accidental file removals some distributions of Linux will ship with an alias for rm with the default `.bashrc` file. This alias gives the interactive `-i` flag for rm, this tells rm to prompt the user before removing files and directories.

    # alias
    alias rm='rm -i'

#### Remove a file without being prompted

While you can simply unalias the rm alias, a simpler and generally used method to remove files without being prompted is to add the force `-f` flag to the rm command. It is advisable that you only add the force `-f` flag if you really know what you are removing.

    # rm -f b-file

#### Remove a file without being prompted and with verbosity

If you don't want to be prompted for each file removable but also want to keep an eye on rm in case the command starts removing unexpected files, you can simply add the verbose `-v` flag.

    # rm -fv c-file
     removed `c-file'

#### Remove multiple files

There are many ways to remove multiple files, one method is to simply list each file you want to remove.

    # rm -f a-file b-file

#### Removing multiple files with a wildcard

The bash command line supports wildcards and regex statements. A simplier way to remove all files that end in the word file is to simply state `*file`. I suggest being cautious with wildcards as it is entirely possible to remove a file without meaning to.

    # rm -f *file

#### Remove files using a regex

Another common method of deleting files is to use regex statement, the below would remove anything that looks like files-0 through files-9 but would not remove files-a or files-list.

    # rm -f files-[0-9]

#### Remove a directory and all of it's contents with rm

If you want to simply remove an entire directory and all of the contents within, including both files and directories the easiest method is to add the recursive `-R` flag to rm. If you are in any way unsure of what you are doing than drop the force `-f` and replace it with verbose `-v` or interactive `-i`.

    # rm -Rf somedir/

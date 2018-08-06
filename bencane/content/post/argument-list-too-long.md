---
authors:
- Benjamin Cane
categories:
- Command Line
- How To and Tutorials
- Linux
- Linux Commands
date: '2011-07-13T03:40:22'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- tech
- unix
title: Argument list too long
url: /2011/07/13/argument-list-too-long

---

If you've been an administrator for long enough eventually you will have run into an issue like so.

    [bcane@bcane toomany]$ rm *  
    bash: /bin/rm: Argument list too long

This can be a confusing issue at first if you've never run into it. The work around is pretty easy but first lets examine why you got this error.

The reason you see Argument list too long is because when you run your command you are passing it too many arguments.

In this case (which is the most common time you will see this) we tried to rm all of the files in my directory which had 300,000 files in it; that was a few too many arguments for rm.

Even though you typed

    [bcane@bcane toomany]$ rm *

When the * is interpreted by bash it becomes

    [bcane@bcane toomany]$ rm file1 file2 file3 file4 file5 [files6 - file299999] file300000

Within the kernel there is a limit to how many arguments you can pass to a command. This is there to prevent misuse of the system by processes that may want to go a little too wild.

Now lets get to the quick workarounds.

## Option 1:

    [bcane@bcane toomany]$ for x in `ls`; do rm $x; done

This is a pretty easy option, Using a for loop every line of output from ls executes an rm.

## Option 2:

    [bcane@bcane toomany]$ ls | xargs rm

This will take the output of ls and send it to the command xargs which will then breakup the output and run multiple rm commands with smaller sets of arguments.

## Option 3:

    [bcane@bcane toomany]$ find ./ -maxdepth 1 -type f -exec rm {} \;

You could also use find with the -exec flag but this can be a little dangerous, if you don't have the -maxdepth option find will also delete files in sub-directories. You may or may not want that.

With that said in certain situations Option 2 and 1 are also dangerous so be careful whenever you are performing file options like the above.

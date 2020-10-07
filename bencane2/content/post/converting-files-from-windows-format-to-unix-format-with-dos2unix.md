---
authors:
- Benjamin Cane
categories:
- Linux
- Unix
date: '2014-02-11T08:00:00'
description: This article explains what end of line characters are and how to use
  dos2unix to convert files that contain Windows EOL characters to a Unix format.
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- dos2unix
- dos end of line characters
- EOL characters
- unix2dos
- working with files in linux
title: Converting files from Windows format to Unix format with dos2unix
url: /2014/02/11/converting-files-from-windows-format-to-unix-format-with-dos2unix

---

Ever run a shell script and get the following error?

    # ./dosfile.sh 
    : bad interpreter: No such file or directory

The error may look like there is a problem with your scripts SHEBANG where you specify the interpreter, so you go look and the line contains `#!/bin/bash` which is correct. So then you start wondering if there is a problem with the `/bin/bash` binary, and all sorts of thoughts of what would happen if `/bin/bash` was missing or broken start racing through your head. Luckily though, the issue isn't that complicated.

## What are EOL characters

The issue has nothing to do with the bash binary at all, but rather the issue is with the contents of the shell script itself. The problem is specifically due to the type of end of line characters in the file. Each operating system has a specific special character that symbolizes the end of a line. 

To help explain how EOL (end of line) characters work, I am going to use a quick `perl` command.

    # perl -e 'print("this is 1\nthis is 2\nthis is 3\n");'
    this is 1
    this is 2
    this is 3

The perl command is pretty basic, it outputs the arguments given to the print function. If you look at the arguments given to print and the output, you will notice a little bit of difference. Every time the characters `\n` are printed a new line is started. This is because `\n` is an escape sequence that is used to symbolize a newline. On Linux and Unix operating systems this "newline" character is a `LF` or Line Feed character. For other Systems such as Windows a newline is defined differently. 

On a Windows/DOS operating system the same print arguments would need to contain `\r\n` to indicate a newline. The `\r\n` escape sequence symbolizes a `CR+LF` or Carriage Return + Line Feed character. In general Linux does not recognize the `\r` or Carriage Return character as an EOL character, because of this a file that contains a Carriage Return can cause problems with some programs/tools.

## Visualizing the EOL characters

Most tools generally do not output EOL characters as these characters are really not meant to be seen. There are however a few commands that will show you the EOL character being used for debugging purposes. The `cat` command is one of these tools, when given the `-e` option `cat` will show a symbol that designates which EOL character was used.

    # cat -e dosfile.sh 
    #!/bin/bash^M$
    #### This is a file^M$
    ##################^M$
    ##################^M$
    ##################^M$
    ^M$
    echo "yay i ran"^M$

As you can see when we use `cat -e` there is an `^M` and a `$` at the end of each line. These characters represent the EOL characters within this file, the `^M` symbolizes a Carriage Return and the `$` symbolizes a Line Feed.

Since Linux recognizes `$` or `LF` as the EOL character, the `^M` or `CR` in this file is seen as part of the line. When Linux executes a script it reads the first line and tries to find which interpreter to run the script against, this line is called the SHEBANG. In this specific file when Linux is reading the file and trying to identify an interpreter it sees `#!/bin/bash^M`, and that is not a valid file.

If we circle back to the original error the message was **"No such file or directory"** which makes sense if you are looking for `#!/bin/bash^M`.

## Converting the EOL characters for Linux/Unix with dos2unix

Luckily, fixing the script doesn't require much effort. The command `dos2unix` can convert the `CR+LF` characters to a Unix friendly `LF` character.

    # dos2unix dosfile.sh 
    dos2unix: converting file dosfile.sh to Unix format ...

If we use `cat -e` to read the file again we can see that only the `$` or `LF` EOL character is on the end of each line.

    # cat -e dosfile.sh 
    #!/bin/bash$
    #### This is a file$
    ##################$
    ##################$
    ##################$
    $
    echo "yay i ran"$

Now that the script has been converted we can run it without error.

    # ./dosfile.sh 
    yay i ran

## Converting the EOL characters for DOS/Windows with unix2dos

While I don't use this command very often, some may find themselves in a situation where they need to convert a file from Linux format to a DOS format. Like the `dos2unix` command there is also a `unix2dos` command that will convert `LF` to `CR+LF` characters. 

    # unix2dos dosfile.sh 
    unix2dos: converting file dosfile.sh to DOS format ...

If we use `cat -e` again we can see the DOS style EOL characters at the end of each line.

    # cat -e dosfile.sh 
    #!/bin/bash^M$
    #### This is a file^M$
    ##################^M$
    ##################^M$
    ##################^M$
    ^M$
    echo "yay i ran"^M$

## A word of advice

The problems with `CR` characters causing issues is not only limited to scripts either, I have seen many problems where a configuration file was not read properly because the file contained DOS style EOL characters. I suggest if you have an environment where Sysadmins, Developers or Database Admins use Windows to create or edit files you should always use `dos2unix` to convert the files before deploying the files to Linux/Unix systems. EOL characters can be very frustrating to troubleshoot as they are not in plain sight; if you ever have an issue where a file isn't read properly, check the EOL characters.

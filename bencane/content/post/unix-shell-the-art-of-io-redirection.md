---
authors:
- Benjamin Cane
categories:
- All Articles
- Command Line
- How To and Tutorials
- Linux
- Linux Commands
- Programming
- Shell Scripting
- Unix
- Unix Commands
date: '2012-04-16T15:38:12'
draft: false
header:
  caption: ''
  image: ''
tags:
- bash
- bash redirection
- linkedin
- linux
- oracle
- osx
- shell
- solaris
- tech
- ubuntu
- unix
title: 'Unix Shell: The Art of I/O Redirection'
url: /2012/04/16/unix-shell-the-art-of-io-redirection

---

One of the primary tricks in my sysadmin bag-o-tricks is Input/Output Redirection; I have found that while many people use Shell I/O Redirection throughout their day not everyone fully understands why and how it works.

## The Input and Output

In the Unix environment there is always 3 streams open stdin, stdout, & stderr; these special streams are used for interacting with the user input and program output within the Unix/Linux shell environment. In addition to files in /dev/ these streams also have a reserved file descriptor attached to them; meaning you can interact with them from the command line.

Before we start showing you how to redirect these streams lets first explain what they are.

**stdin - Standard Input**

This stream is used to get input for commands from the user keyboard.
stdin has the file descriptor of 0 and a file of /dev/stdin.

**stdout - Standard Output**

This stream is used for non-error output from programs.
stdout has the file descriptor of 1 and a file of /dev/stdout.

**stderr - Standard Error**

This stream is used for error output from programs.
stderr has the file descriptor of 2 and a file of /dev/stderr.

## Examples of Input and Output

To explain the interaction better I am going to use the following text formats.

    **stdin**
    -stdout-
    _stderr_

When cat is run without giving it a filename the cat program opens and expects user input.

     madflojo@netbook:~$ cat

Whatever text I type with my keyboard is considered Standard Input; the cat command will send my input out as Standard Output.
     
     madflojo@netbook:~$ cat
     **Say hello netbook**
     -Say hello netbook-

When a program in the Unix environment prints errors or diagnostic information it uses the Standard Error stream rather than Standard Output; This helps prevent mixing a commands errors with the same commands output.
     
     madflojo@netbook:~$ cat ./stuff
     _cat: ./stuff: No such file or directory_

### Redirection

How is all of this useful? Well the various Input and Output methods become extremely useful when using the redirect features of the Unix/Linux shell programs. For example, what happens when you want to take the output (stdout) of one program and write it to a file? Well you can use that by using special Redirection Operators designated within your shell.

#### Redirect to a file
     
     program > file

The > (left caret) symbol is used to redirect to a file; but be warned that a single left caret will truncate the file, then enter the redirected data into the file; this effectively replaces your data. If the designated file does not exist the file will be created.

The > symbol will redirect stdout by default but you can specify whether to redirect stdout or stderr by putting the appropriate file descriptor in front of the redirect symbol.
     
     1> - Redirects stdout (default)
     2> - Redirects stderr
     
**Example:**

     madflojo@netbook:~$ echo test > /tmp/filename
     madflojo@netbook:~$ cat /tmp/filename
     test

#### Redirect to a file but append the data
     
     program >> file

When two > (left caret) symbols are used the output that is being redirected is appended to the file rather than overwriting the file entirely. Again the file descriptor can be used to specify whether to write stdout or stderr to the file specified.
     
     madflojo@netbook:~$ cat ./stuff 2>> /tmp/filename
     madflojo@netbook:~$ cat /tmp/filename
     test
     cat: ./stuff: No such file or directory

#### Redirect input from a file
     
     program < file

Much like the > (left caret) the < (right caret) can be used to redirect stdin from a file to a program.
     
     madflojo@netbook:~$ cat < /tmp/filename
     test 
     cat: ./stuff: No such file or directory

#### Pipe output from one program to another
     
     program | program

The | (pipe) is used to redirect stdout from one command to stdin for another. The | (pipe) is not considered a Redirect Operator but rather a Control Operator; while | (pipe) is used to redirect output not all Control Operators have this function.
     
     madflojo@netbook:~$ ls /tmp/ | grep filename
     filename

#### Redirect stderr to stdout
     
     program > filename 2>&1

When using redirects you can use the &N (where N = file descriptor) to redirect 2 methods of output to the same path. In my example above I am redirecting the stderr to the file; This can also be used with the | (pipe) control operator.
     
     madflojo@netbook:~$ ls /tm/ /tm2/ 2>&1 | grep 2
     ls: cannot access /tm2/: No such file or directory

#### Write to a file and stdout
     
     program | tee filename

While tee is neither a control or redirection operator I feel it deserves being mentioned. Tee is a command that will take the stdin given to it and write that to both the file specified and to stdout. I find this extremely useful when running a command that you both want to log the output and see the output on your screen.
     
     madflojo@netbook:~$ ls | tee -a filelist.txt
     Desktop
     Documents
     Downloads
     madflojo@netbook:~$ ls -la filelist.txt
     -rw-rw-r-- 1 madflojo madflojo 113 2012-04-15 22:01 filelist.txt

If the `-a` flag is added to tee the command will append the output to the file specified rather than overwriting.

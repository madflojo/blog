---
authors:
- Benjamin Cane
categories:
- Linux
date: '2014-04-01T08:55:00'
description: This article covers the Linux kill command and how it sends signals to
  terminate processes. Also why you should avoid using kill -9.
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- redhat
- centos
- ubuntu
- signal
- kill
- linux kill
- kill processes
- killall
- linux processes
- sigkill
- sigterm
- sigquit
- sighup
title: Understanding the kill command, and how to terminate processes in Linux
url: /2014/04/01/understanding-the-kill-command-and-how-to-terminate-processes-in-linux

---

One of my biggest pet peeves as a Linux sysadmin is when I see users, or even other sysadmins using `kill -9` on the first attempt to terminate a process. The reason this bugs me so much is because it shows either a lack of understanding of the `kill` command or just plain laziness. Rather than going on a long rant about why this is bad, I wanted to write an article about the `kill` command and how **signal** works in Linux.

## Using the kill command

In Linux and Unix when you want to stop a running process you can use the `kill` command via the command line interface. The `kill` command in it's most basic form is pretty simple to work with, if you want to terminate a process you simply need to know the processes id number. 

### Finding the PID of a running process

To find the process id or PID of a running process we will use the `ps` command. This command will list running processes and some information about those processes. The `ps` command has many options and many methods of showing processes; I could dedicate an article just to `ps`. For this example, I am just going to use the `ps` command with the `-C` flag, this flag can be used to lookup a process by the name of the command thats being run.

**Syntax:**

    # ps -C <command>

**Example:**

		# ps -C nginx
		  PID TTY          TIME CMD
		  566 ?        00:00:00 nginx
		  567 ?        00:00:00 nginx
		  568 ?        00:00:06 nginx
		  570 ?        00:00:06 nginx
		  571 ?        00:00:06 nginx

In the above example I am using the `ps` command to search for nginx processes. If you look at the output you will see that the PID for each process is listed in the first column. We will use these numbers to kill the nginx processes.

### Killing a process with kill

Now that we have found the PID of the process we want to stop, we can use the `kill` command to terminate the process.

**Syntax:**

    # kill <pid>

**Example:**

		root@blog:/# ps -C nginx
		  PID TTY          TIME CMD
		  566 ?        00:00:00 nginx
		  567 ?        00:00:00 nginx
		  568 ?        00:00:08 nginx
		  570 ?        00:00:09 nginx
		  571 ?        00:00:08 nginx
		root@blog:/# kill 571
		root@blog:/# ps -C nginx
		  PID TTY          TIME CMD
		  566 ?        00:00:00 nginx
		  567 ?        00:00:00 nginx
		  568 ?        00:00:08 nginx
		  570 ?        00:00:09 nginx
		 8347 ?        00:00:00 nginx

As you can see in the example by running kill with the 571 PID it stopped the nginx process with a process id of 571. Now it is good to note that another nginx process took the place of the process I killed, this is because I killed a worker process for nginx. In order to stop nginx completely I would need to kill the master nginx process.

## Using signals with kill

A somewhat common (though if it happens to you a lot, than that may be sign that something is wrong) issue is when you run `kill <pid>` on a process and the process does not terminate. This can happen for many reasons but what can you do in those scenarios? Well a common response is to use the `kill` command with the `-9` flag. 

**Example:**

		root@blog:/# ps -C nginx
		  PID TTY          TIME CMD
		  566 ?        00:00:00 nginx
		  567 ?        00:00:00 nginx
		  568 ?        00:00:09 nginx
		  570 ?        00:00:09 nginx
		 8347 ?        00:00:00 nginx
		root@blog:/# kill -9 570
		root@blog:/# ps -C nginx
		  PID TTY          TIME CMD
		  566 ?        00:00:00 nginx
		  567 ?        00:00:00 nginx
		  568 ?        00:00:09 nginx
		 8347 ?        00:00:00 nginx
		 8564 ?        00:00:00 nginx

So why does `-9` work? Well when the `kill` command is run it is actually sending a [singal](http://man7.org/linux/man-pages/man7/signal.7.html) to the process. By default the `kill` command will send a `SIGTERM` signal to the specified process. 

The `SIGTERM` signal tells the process that it should perform it's shutdown proceedures to terminate the process cleanly by closing all log files, connections, etc. The below example is a excerpt of a python application, this snippet of code enables the python application to capture the `SIGTERM` signal and perform the actions in the `killhandle` function.

**Signal handling in Python:**

		def killhandle(signum, frame):
		  ''' This will close connections cleanly '''
		  line = "SIGTERM detected, shutting down"
		  syslog.syslog(syslog.LOG_INFO, line)
		  rdb_server.close()
		  syslog.closelog()
		  sys.exit(0)
		
		signal.signal(signal.SIGTERM, killhandle)

In the above code example the process is able to close both it's database connection and connection to rsyslog cleanly before exiting. In general it is a good idea for applications to close open file handles and external connections during shutdown, however sometimes these processes can either take a long time or due to other issues not happen at all. Leaving the process in a state where it is not correctly running but also not terminated.

When a process is in a limbo state it is reasonable to send the process the `SIGKILL` signal, which can be invoked by running the `kill` command with the `-9` flag. Unlike `SIGTERM` the `SIGKILL` signal cannot be captured by the process and thus it cannot be ignored. The `SIGKILL` signal is handled outside of the process completely, and is used to stop the process immediately. The problem with using `SIGKILL` is that it does not allow an application to close its open files or database connections cleanly and over time could cause other issues; therefor it is generally better to reserve the `SIGKILL` signal as a last resort.

### Signal Numbers and Dispositions

Each **signal** has a numeric Value and an Action associated to it, the numeric values can be used with commands such as `kill` to define which signal is sent to the process. Each signal also has an **"action"** or **"disposition"** associated with it which defines what type of action this signal should invoke.

#### Signal Actions

While there are several **actions** for the various signals on a Linux system, I want to highlight the below as they are the most commonly used signals from a process termination perspective.

  * **Term** - This action is used to signal that the process should terminate
  * **Core** - This action is used to signal that the process should core dump and then terminate

#### Common Signals

Below is a list of a few common signals, the numeric value of that signal, the action that is associated with it and how to send that signal to a process. This list, while not complete, should cover general usage of the `kill` command.

`SIGHUP` **- 1 - Term**

  * The `SIGHUP` signal is commonly used to tell a process to shutdown and restart, this signal can be caught and ignored by a process.

**Syntax:**

    # kill -1 <pid>
    # kill -HUP <pid>
    # kill -SIGHUP <pid>


`SIGINT` **- 2 - Term**

  * The `SIGINT` signal is commonly used when a user presses `ctrl+c` on the keyboard.

**Syntax:**

    # kill -2 <pid>
    # kill -INT
    # kill -SIGINT


`SIGQUIT` **- 3 - Core**

  * The `SIGQUIT` signal is useful for stopping a process and telling it to create a core dump file. The core file can be useful for debugging applications but keep in mind your [system needs to be setup](http://bencane.com/2011/09/22/kill-creating-a-core-dump/) to allow the creation of core files.

**Syntax:**

    # kill -3 <pid>
    # kill -QUIT <pid>
    # kill -SIGQUIT <pid>


`SIGKILL` **- 9 - Term**

  * The `SIGKILL` signal cannot be ignored by a process and the termination is handled outside of the process itself. This signal is useful for when an application has stopped responding or will not terminate after being given the `SIGTERM` command. This signal should stop more processes however there are exceptions, such as [zombie processes](http://bencane.com/2012/07/02/when-zombies-invade-linux-what-are-zombie-processes-and-what-to-do-about-them/).

**Syntax:**

    # kill -9 <pid>
    # kill -KILL <pid>
    # kill -SIGKILL <pid>


`SIGSEGV` **- 11 - Core**

  * The `SIGSEGV` signal is generally sent to a process by the kernel when the process is misbehaving, it is used when there is an "Invalid memory reference" and you may commonly see a message such as `segmentation fault` in log files or via `strace`. You can also technically call this signal with `kill` as well; however it is mainly useful for creating core dump files, which can also be performed by using the `SIGQUIT` signal.

**Syntax:**

    # kill -11 <pid>
    # kill -SEGV <pid>
    # kill -SIGSEGV <pid>


`SIGTERM` **- 15 - Term**

  * The `SIGTERM` signal is the default signal sent when invoking the kill command. This tells the process to shutdown and is generally accepted as the signal to use when shutting down cleanly. Technically this signal can be ignored, however that is considered a bad practice and is generally avoided.

**Syntax:**

    # kill <pid>
    # kill -15 <pid>
    # kill -TERM <pid>
    # kill -SIGTERM <pid>


It is a good idea for any sysadmin to get familiar with how signal works (`man 7 signal`) and what each signal really means, but if you are looking for the TL;DR version. Don't run `kill -9` unless you really have to. If the process isn't stopping right away give it a bit more time, or try to find out if the process is waiting on a child process to finish before running `kill -9`.

---
authors:
- Benjamin Cane
categories:
- How To and Tutorials
- Linux
- Linux Threads
date: '2011-06-25T01:24:50'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- tech
title: Checking the number of LWP (threads) in Linux
url: /2011/06/25/checking-the-number-of-lwp-threads-in-linux

---

Linux has these nice little processes called **LWP** (Light Weight Process) or otherwise known as threads. Generally these are spawned by 1 master process that will show up in your normal ps output.

    # ps -elf | wc -l  
    145

So does this mean your system only has 145 processes running? No. If you run ps with a -T you will see all of the threads as well.

    # ps -elfT | wc -l  
    275

As you can see the process count jumped significantly due to threads. Normally this is never any type of problem, However sometimes a process (usually java based) will have a thread leak. This can cause your system to run into system limits.

Specifically one limit I have seen systems hit is the `kernel.pid_max` limit.

    # sysctl -a | grep kernel.pid_max  
    kernel.pid_max = 32768

As you can see on my system the pid_max is **32768**, this means the system can only give out 32768 PID's at one time (it will rollover if pid #'s are available).

The reason threads come into play here is because each thread has a PID, and SPID number. The SPID's also take from the pid_max number.

To see the number of threads one specific process is using you can do the following.

    # ps -p 2089 -lfT  
    F S UID PID SPID PPID C PRI NI ADDR SZ WCHAN STIME TTY TIME CMD  
    0 S bcane 2089 2089 1 0 80 0 - 29457 poll_s 09:17 ? 00:00:09 gnome-terminal  
    1 S bcane 2089 2091 1 0 80 0 - 29457 poll_s 09:17 ? 00:00:00 gnome-terminal  
    1 S bcane 2089 2094 1 0 80 0 - 29457 pipe_w 09:17 ? 00:00:00 gnome-terminal
  
The lesson for today, is watch your threads!

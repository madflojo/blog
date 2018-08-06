---
authors:
- Benjamin Cane
categories:
- All Articles
- Command Line
- How To and Tutorials
- Linux
- Linux Commands
- SysAdmin Basics
- Unix
- Unix Commands
date: '2013-09-09T09:24:03'
description: How to set a CPU priority (niceness) value with the nice and renice commands
draft: false
header:
  caption: ''
  image: ''
tags:
- bash
- change process niceness
- cpu
- cpu priority
- linux
- linux niceness
- linux os
- linux scheduler
- nice
- niceness
- processes
- renice
- unix
title: Setting process CPU priority with nice and renice
url: /2013/09/09/setting-process-cpu-priority-with-nice-and-renice

---

Nice is a command in Unix and Linux operating systems that allows for the adjustment of the "Niceness" value of processes. Adjusting the "niceness" value of processes allows for setting an advised CPU priority that the kernel's scheduler will use to determine which processes get more or less CPU time. In Linux this niceness value can be ignored by the scheduler, however other Unix implementations can treat this differently.

Being able to adjust the niceness value comes in handy in two scenarios usually.

The first is when you have a process that is or may cause resource contention; for this scenario we would increase the processes niceness value.

The second is when you want to increase the resources of a specific process in order to decrease the run time or give a process higher priority. For this scenario we would decrease the processes niceness value.

## Finding the current niceness value

Before we start changing niceness values I want to go over identifying what the current nice values are.

### Determining the default niceness value of new processes

Different OS distributions can have different default values for new processes. The simplest method to determine the default value is to simply run the nice command with no arguments. By default nice will simply return the current niceness value.

**Example:**

    $ nice
    0

In this example we see the niceness value of 0 is the default.

### Determining the niceness value of a current process

The niceness value of current processes are also pretty simple to find as they are visible in the ps command's long format.

In the below example we are going to find the current niceness value of the sshd (PID 941) process.

    $ ps -lp 941
    F S UID PID PPID C PRI NI ADDR SZ WCHAN TTY TIME CMD
    4 S 0 941 1 0 70 -10 - 1713 poll_s ? 00:00:00 sshd

Just in case the formatting of this post doesn't make it easy to see, the column `NI` is the niceness value of the sshd process. In this case it is currently set to `-10`.

## Making a process nicer, decreasing the CPU Priority

Niceness values range from -20 (the highest priority, lowest niceness) and 19 (the lowest priority, highest niceness). In order to prevent a process from stealing CPU time from high priority processes, we will increase the processes niceness value.

### Changing the nice value of a new process

Changing the niceness value of a new process is fairly simple. The nice command itself will run the supplied command with the desired niceness value.

**Example:**

    $ nice -n 19 ./test.sh 
    My niceness value is 19

This method is helpful for CPU intensive processes that are not as time sensitive as other processes running on the system. By increasing the niceness value, we allow other processes on the system to be scheduled more frequently. I do want to highlight again that while this value is adjustable it can be ignored by the kernel's scheduler in Linux implementations.

### Changing the nice value of a running process

To change the niceness value of a running process we will utilize the renice command. The usage is similar to nice however rather than supplying a command to run we will be supplying a process id.

In this example we will be adjusting the priority of the sshd process I showed above.

    # renice -n 10 -p 941
    941 (process ID) old priority -10, new priority 10

It is important to note that only the root user can modify the niceness value of other users processes. However a regular unprivileged user can adjust the niceness value to a "nicer" value on processes owned by that user.

## Making a process less nice, increasing CPU priority

Now that we have adjusted processes to becoming nicer to the system, let us make a process that is less nice. By changing the priority of a process to a negative number, we are suggesting to the scheduler that it should provide higher priority to the specified process.

### Changing the nice value of a new process

The method of changing a process to be less nice is the same as making a process nicer.

**Example:**

    # nice -n -20 ./test.sh 
    My niceness value is -20

### Changing the nice value of a running process

To change the niceness of a running process to a negative value we will use the renice command again.

    # renice -n -10 -p 941
    941 (process ID) old priority 10, new priority -10

It is important to note that changing a processes niceness value to a negative value requires root privileges. As the effects of giving a process a higher priority could have detrimental effects on a system.

It is advisable to reserve setting niceness values to -20 only when absolutely necessary; as this would suggest to the kernel scheduler that the specified process has the same CPU priority as kernel worker threads.

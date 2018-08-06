---
authors:
- Benjamin Cane
categories:
- Administration
- All Articles
- Linux
- Troubleshooting
date: '2012-07-02T16:55:46'
draft: false
header:
  caption: ''
  image: ''
tags:
- init
- linkedin
- linux
- linux os
- orphaned process
- process
- tech
- troubleshooting
- unix
- zombie
- zombie processes
title: 'When Zombies Invade Linux: What are Zombie Processes and What to do about
  them'
url: /2012/07/02/when-zombies-invade-linux-what-are-zombie-processes-and-what-to-do-about-them

---

Zombies don't just appear in scary movies anymore, sometimes they also appear on your Linux systems; but don't fret they are mostly harmless.

## What is a Zombie Process?

Before we get started I wanted to first cover what exactly a Zombie process is.

Linux and Unix both have the ability for a process to create a sub process otherwise known as a "Child Process". Once a process creates a new sub process the first process then becomes a "Parent Process" as it has spawned a child process during its execution.

A Zombie or defunct process is a process that has finished its execution and is waiting for its Parent Process to read its exit status. Because the child process has finished, it is technically a "dead" process however since it is waiting for its parent there is still an entry in the process table. The zombie's parent process does not necessarily need to be running for a zombie to appear, however it is most common to see a zombie process whose parent has died unexpectedly.

### How to spot a Zombie Process

Zombie processes can be found easily with the ps command. Within the ps output there is a `STAT` column which will show the processes current status, a zombie process will have `Z` as the status. In addition to the `STAT` column zombies commonly have the words `<defunct>` in the `CMD` column as well.

**Example:**
     
     $ ps -elf | grep Z
     F S UID PID PPID C PRI NI ADDR SZ WCHAN STIME TTY TIME CMD
     1 Z madflojo 28827 28821 0 80 0 - 0 exit 12:28 pts/4 00:00:00 [zombies.aahhh]
     1 Z madflojo 28828 28821 0 80 0 - 0 exit 12:28 pts/4 00:00:00 [zombies.aahhh]
     1 Z madflojo 28829 28821 0 80 0 - 0 exit 12:28 pts/4 00:00:00 [zombies.aahhh]
     1 Z madflojo 28830 28821 0 80 0 - 0 exit 12:28 pts/4 00:00:00 [zombies.aahhh]
     1 Z madflojo 28831 28821 0 80 0 - 0 exit 12:28 pts/4 00:00:00 [zombies.aahhh]

## What is the difference between a Zombie and Orphaned Process?

Orphaned processes are very similar to Zombie processes; however there is one major difference. An Orphaned process is a child process that is still an active process whose parent has died. Unlike zombies the orphaned process will be reclaimed or adopted by the init process.

### How to spot an Orphaned Process

Orphaned processes can be found easily with the ps command as well. Within the ps output there is a `PPID` column which will show the processes parent process id; a orphaned process will have the PPID of `1` which is the `init` process.

You may be thinking to yourself, how do I differentiate an Orphaned process from a Daemon process? Well in short, there is no difference. For all intents and purposes a daemon process is a orphaned process, however the exiting of the parent process is on purpose rather than by error.

**Example:**
     
     $ ps -elf | grep sshd
     4 S root 718 1 0 80 0 - 12487 poll_s Jun07 ? 00:00:00 /usr/sbin/sshd -D

## What to do about Zombie Processes?

Before performing any activity to clean up zombie processes it is best to identify the root cause of the issue. Zombie processes do not indicate a normal state for your system, they may be benign for now however like real zombies they become more troublesome when they are in large numbers. They also indicate either a system issue or an application issue depending on the source of the processes.

The steps necessary to clean up zombie processes is complicated and very situational, below are a couple of high level answers that can guide you to a solution.

### If the parent process is still active

If the parent process of the zombie or zombies is still active **(not process id 1)** than this is an indication that the parent process is stalled on a certain task and has not yet read the exit status of the child processes. At this point the resolution is extremely situational, you can use the **[strace](http://bencane.com/2012/03/advanced-linux-troubleshooting-strace/)** command to attach to the parent process and troubleshoot from there.

You may also be able to make the parent process exit cleanly taking its zombie children with it by issuing the kill command. If you do run the `kill` command I suggest that you run a `kill` with the default signal `-15 (SIGTERM)` rather than using a  `-9 (SIGKILL)`; as   SIGTERM  will tell the parent process to exit cleanly which is more likely to read the exit status of the zombie children.

### If the parent process is no longer active

If the parent process is no longer active than the clean up activity becomes a choice; at this point you can leave the zombie processes on your system, or you can simply reboot. A Zombie process whose parent is no longer active is not going to be cleaned up without rebooting the system. If the zombie processes are only in small numbers and not reoccurring or multiplying than it may be best to leave these processes be until the next reboot. If however they are multiplying or in a large number than this is an indication that there is a significant issue with your system.

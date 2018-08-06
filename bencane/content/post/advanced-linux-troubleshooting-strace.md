---
authors:
- Benjamin Cane
categories:
- Administration
- All Articles
- Linux
- Linux Commands
- Troubleshooting
date: '2012-03-24T19:33:45'
draft: false
header:
  caption: ''
  image: ''
tags:
- kernel
- linkedin
- linux
- redhat
- strace
- tech
- troubleshooting
- troubleshooting linux
- unix
title: Linux Troubleshooting with strace
url: /2012/03/24/advanced-linux-troubleshooting-strace

---

Today I want to cover one of the best troubleshooting tools in any sysadmins arsenal; strace. Strace is a command that will trace the system calls and signals from a specified command. What does that mean in layman's terms? Strace will output all of the inner workings of a process you run it against.

If a process opens a file or binds a port, strace will print that action; it is a great utility for troubleshooting when a process is not behaving as expected and you can't find any reason in the commands output or log files.

Below is a real scenario that happened to me a few weeks ago.

## The Issue

When trying to start vsftpd with the service command (or systemctl on newer versions) the daeomon would fail to start.
     
     [root@laptop ~]# systemctl start vsftpd.service
     Job failed. See system logs and 'systemctl status' for details.

     [root@laptop ~]# systemctl status vsftpd.service
     vsftpd.service - Vsftpd ftp daemon
     	  Loaded: loaded (/lib/systemd/system/vsftpd.service; disabled)
     	  Active: failed since Sat, 24 Mar 2012 11:55:25 -0700; 2min 28s ago
     	 Process: 19356 ExecStart=/usr/sbin/vsftpd /etc/vsftpd/vsftpd.conf (code=exited, status=1/FAILURE)
     	  CGroup: name=systemd:/system/vsftpd.service

As you can see the output of these commands are not very descriptive as to why vsftpd will not start. So I started looking at the log files; vsftpd does not have many log files configured by default but I checked both the xferlog and the messages just in case I could find a clue as to why it did not start.

After the log files didn't give me anything useful, I started looking at the /etc/vsftpd/vsftpd.conf file because I knew some of my colleagues were tinkering with it on this server recently. After a little review the configuration file looked normal and did not have anything odd in it. Just in case though I replaced the configuration file with the default file and tried to restart vsftpd; again the service did not start.

This told me that my issue was not with the configuration of vsftpd.

I decided to try starting vsftpd manually via the command line hoping that will output a useful error (sometimes this works).
     
     [root@laptop ~]# /usr/sbin/vsftpd /etc/vsftpd/vsftpd.conf
     [root@laptop ~]# ps -elf | grep vsftpd
     0 S root     19435 19077  0  80   0 -  1147 pipe_w 12:05 pts/1    00:00:00 grep --color=auto vsftpd

As you can see from the output I recieved even less information from trying to start vsftpd manually.

## Using strace for troubleshooting

At this point I called in my trusty friend strace.

The syntax of strace is pretty straight forward you simply put `strace <command line>` however I am going to use the `-f` flag which allows strace to also display the system calls and signals of child processes started by the command you provided.
     
     [root@laptop ~]# strace -f /usr/sbin/vsftpd /etc/vsftpd/vsftpd.conf
     <truncated output (it is seriously a lot of output)>
     [pid 19499] socket(PF_INET, SOCK_STREAM, IPPROTO_TCP) = 3
     [pid 19499] setsockopt(3, SOL_SOCKET, SO_REUSEADDR, [1], 4) = 0
     [pid 19499] rt_sigaction(SIGCHLD, {0xf5ac00, ~[RTMIN RT_1], 0}, NULL, 8 ) = 0
     [pid 19499] rt_sigaction(SIGALRM, {0xf5abd0, ~[RTMIN RT_1], 0}, NULL, 8 ) = 0
     [pid 19499] rt_sigaction(SIGHUP, {0xf5ac00, ~[RTMIN RT_1], 0}, NULL, 8 ) = 0
     [pid 19499] rt_sigaction(SIGALRM, {0xf5abd0, ~[RTMIN RT_1], 0}, NULL, 8 ) = 0
     [pid 19499] bind(3, {sa_family=AF_INET, sin_port=htons(21), sin_addr=inet_addr("0.0.0.0")}, 16) = -1 EADDRINUSE (Address already in use)
     [pid 19499] fcntl64(0, F_GETFL)         = 0x8002 (flags O_RDWR|O_LARGEFILE)
     [pid 19499] fcntl64(0, F_SETFL, O_RDWR|O_NONBLOCK|O_LARGEFILE) = 0
     [pid 19499] write(0, "500 OOPS: ", 10)  = 10
     [pid 19499] write(0, "could not bind listening IPv4 so"..., 36) = 36
     [pid 19499] write(0, "rn", 2)         = 2
     [pid 19499] exit_group(1)               = ?
     Process 19499 detached

The output of strace'ing vsftpd is quite a bit and to be honest is pretty confusing for those who are not familiar with the different system calls. But even if you are not familiar with system calls, strace can help you. When reviewing the output of strace you simply look for words that suggest an error.

As a caveat when you see the process not able to open a file that does not necessarily mean this is the cause of your issue.

    open("/foo/bar", O_RDONLY) = -1 ENOENT (No such file or directory)

I highlighted the key messages from my strace above, specifically the message that says **"could not bind listening IPv4 so"** and **"Address already in use"**. These messages told me that the vsftpd daemon could not start listening on the local IP with port 21.

After checking netstat I found there is another process already listening on port 21.
     
     [root@laptop ~]# netstat -nap | grep :21
     tcp        0      0 0.0.0.0:21                  0.0.0.0:*                   LISTEN      19212/vs-something

Since there was already a process listening on port 21, vsftpd could not bind the port and hence it could not start. Though it could have been nicer about telling me why it didn't start!

In my real situation inetd has ftp enabled but I was starting vsftpd with the service command.

After identifying the offending process I killed it (as it shouldn't have been running) and configured the system so that the process would not start again and vsftpd would start normally.

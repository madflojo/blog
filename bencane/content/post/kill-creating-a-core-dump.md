---
authors:
- Benjamin Cane
categories:
- All Articles
- Command Line
- How To and Tutorials
- Linux
- Linux Commands
- Troubleshooting
- Unix
- Unix Commands
date: '2011-09-22T22:24:55'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- tech
- troubleshooting
- unix
title: 'kill: Creating a core dump'
url: /2011/09/22/kill-creating-a-core-dump

---

Sometimes when dealing with application problems you run into a point where logs and environmental data just don't seem to provide you with the exact issue.

For this reason there are many times where a developer may ask you to create a core file for their application. Core files contain a lot of very good information around the application such as process information and the data stored in memory. Sometimes this can be the difference in finding the issue and not finding the issue.

**Below are the steps to manually create a core file from a running process.**

Before creating a core file you should check your user limits settings to ensure that core files can be created.

    [bcane@bcane ~]$ ulimit -c
    0

The above setting disables the creation of core files. This setting is a size limit to the core file, if it is 0 then it cannot create a core file. You can also change this setting by running the following.

    [bcane@bcane ~]$ ulimit -c unlimited
    [bcane@bcane ~]$ ulimit -c
    unlimited

It is important that you do this as the user the application runs as and before you start the application in the same session. This setting is inherited by the application, so what ever the ulimit is set as before starting the application is what the ulimit setting will be for the application (unless a start script changes it).

You may also need to edit the `/etc/security/limits.conf` file to enable the application user to modify this setting as well.

After setting ulimit you can create a core file by using `kill -3` which will send the application a SIGQUIT signal.

    [bcane@bcane ~]$ firefox &
    [1] 6314
    [bcane@bcane ~]$ ps -elf | grep firefox
    0S bcane 6314 2113 7 80 0 - 61794 poll_s 11:59 pts/0 00:00:00 /usr/lib/firefox-3.6/firefox
    0S bcane 6348 2113 0 80 0 - 1104 pipe_w 11:59 pts/0 00:00:00 grep color=auto firefox
    [bcane@bcane ~]$ kill -3 6314
    [bcane@bcane ~]$ ls -la core.6314
    -rw-. 1 bcane bcane 129515520 Sep 2211:59 core.6314
    [1]+ Quit (core dumped) firefox

Some items to watch out for with this is to ensure that the core file does not fill up the filesystem. As you can see in my example the file is 124M and that is because it dumps the memory the application is using to disk as well as other information.

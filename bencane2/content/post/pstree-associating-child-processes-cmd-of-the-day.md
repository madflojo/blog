---
authors:
- Benjamin Cane
categories:
- Command Line
- Linux
- Linux Commands
date: '2011-08-13T20:30:06'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- tech
- unix
title: 'pstree: Associating Child Processes'
url: /2011/08/13/pstree-associating-child-processes-cmd-of-the-day

---

Sometimes tracking down which process spawned a child process can be an arduous task, especially when you've reached more than 5 parent processes. To alleviate some of that headache Unix/Linux has a command called pstree which will show processes in a tree format.

**Example:**

    [root@bcane ~]# pstree  
    initNetworkManagerdhclient  
      [{NetworkManager}]  
     [VBoxClient{VBoxClient}]  
     VBoxService6*[{VBoxService}]  
     abrtd  
     anacron  
     atd  
     auditdaudispdsedispatch  
       {audispd}  
      {auditd}

This is awesome if you are trying to find where a process originally spawned from. Below is a couple of flags I like to add to pstree to make it even more helpful.

    -a Show command line arguments. If the command line of a process is swapped out, that process is shown in parentheses. -a implicitly disables compaction for processes but not threads.
    -l Display long lines. By default, lines are truncated to the display width or 132 if output is sent to a non-tty or if the display width is unknown.
    -p Show PIDs. PIDs are shown as decimal numbers in parentheses after each process name. -p implicitly disables compaction.


**Example Output:**


    [root@bcane ~]# pstree -alp  
    init,1  
     NetworkManager,1108 --pid-file=/var/run/NetworkManager/NetworkManager.pid  
      dhclient,2333 -d -4 -sf /usr/libexec/nm-dhcp-client.action -pf /var/run/dhclient-eth0.pid -lf /var/lib/dhclient/dhclient-3d1ab9ed-cb4e-442d-8a32-a953a0d58b64-eth0.lease -cf /var/run/nm-dhclient-eth0.conf eth0  
      {NetworkManager},1122  
      {NetworkManager},1147  
     VBoxClient,1806 --clipboard  
      {VBoxClient},1815  
     VBoxClient,1813 --display  
      {VBoxClient},1816  
     VBoxClient,1819 --seamless  
      {VBoxClient},1820  
     VBoxService,1375  
      {VBoxService},1376  
      {VBoxService},1377  
      {VBoxService},1378  
      {VBoxService},1379  
      {VBoxService},1380  
      {VBoxService},1381  
  





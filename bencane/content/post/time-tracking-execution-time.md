---
authors:
- Benjamin Cane
categories:
- All Articles
- Command Line
- Linux
- Linux Commands
date: '2011-08-27T20:33:05'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- tech
- unix
title: 'time: Tracking execution time'
url: /2011/08/27/time-tracking-execution-time

---

Many times in my life as a sysadmin I've needed to time how long a script or process takes to run. This was usually a manual task until I found the awesomeness of the time command.

**Example:**

    [bcane@bcane ~]$ w  
    09:51:24 up 4:41, 2 users, load average: 0.00, 0.01, 0.05  
    USER TTY FROM LOGIN@ IDLE JCPU PCPU WHAT  
    bcane tty1 :0 18Aug11 8days 3.40s 0.06s pam: gdm-passwo  
    bcane pts/0 :0.0 18Aug11 0.00s 0.03s 0.01s w


    [bcane@bcane ~]$ time w  
    09:52:58 up 4:42, 2 users, load average: 0.00, 0.01, 0.05  
    USER TTY FROM LOGIN@ IDLE JCPU PCPU WHAT  
    bcane tty1 :0 18Aug11 8days 3.46s 0.06s pam: gdm-passwo  
    bcane pts/0 :0.0 18Aug11 0.00s 0.02s 0.00s w  
      
    real 0m0.022s 
    user 0m0.002s 
    sys 0m0.011s

Or if you want to get fancy you can encapsulate the commands with curly brackets.

    [bcane@bcane ~]$ time { for x in /tmp/v*; do sleep 5; echo $x; done; }  
    /tmp/virtual-bcane.Bkon89  
    /tmp/virtual-bcane.v9Bm6L  
    /tmp/virtual-bcane.WXwFtb  
      
    real 0m15.072s  
    user 0m0.001s  
    sys 0m0.006s  

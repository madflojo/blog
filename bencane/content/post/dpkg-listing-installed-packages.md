---
authors:
- Benjamin Cane
categories:
- All Articles
- Command Line
- Linux
- Linux Commands
- Linux Distributions
- Ubuntu
date: '2011-08-27T05:47:00'
draft: false
header:
  caption: ''
  image: ''
tags:
- debian
- linux
- tech
title: 'dpkg: Listing installed packages'
url: /2011/08/27/dpkg-listing-installed-packages

---

If you want to check what packages are installed on a debian based machine you can use `dpkg`.

    slize:~# dpkg --list  
    Desired=Unknown/Install/Remove/Purge/Hold  
    | Status=Not/Inst/Cfg-files/Unpacked/Failed-cfg/Half-inst/trig-aWait/Trig-pend  
    |/ Err?=(none)/Hold/Reinst-required/X=both-problems (Status,Err: uppercase=bad)  
    ||/ Name Version Description  
    +++-===========================================  
    ii adduser 3.110 add and remove users and groups  
    ii apache2 2.2.9-10+lenny7 Apache HTTP Server metapackage  
    ii apache2-mpm-prefork 2.2.9-10+lenny7 Apache HTTP Server - traditional non-threaded model

Or if you are looking for a specific package you can put the name after the command.

    slize:~# dpkg --list apache2  
    Desired=Unknown/Install/Remove/Purge/Hold  
    | Status=Not/Inst/Cfg-files/Unpacked/Failed-cfg/Half-inst/trig-aWait/Trig-pend  
    |/ Err?=(none)/Hold/Reinst-required/X=both-problems (Status,Err: uppercase=bad)  
    ||/ Name Version Description  
    +++-=============================================================-ii  
    apache2 2.2.9-10+lenny7 Apache HTTP Server metapackage

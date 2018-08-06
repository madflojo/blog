---
authors:
- Benjamin Cane
categories:
- Command Line
- Linux
- Linux Commands
- Unix
- Unix Commands
date: '2011-08-03T07:05:00'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- redhat
- rpm
- tech
- yum
title: Finding what installed a binary with YUM and RPM
url: /2011/08/03/finding-what-installed-a-binary-with-yum-and-rpm

---

Ever find yourself wondering what package installed a binary on your Red Hat or Red Hat like distro's? Well you can find that out pretty easily using yum or rpm.

    [root@bcane ~]# yum whatprovides /usr/bin/ssh
    Loaded plugins: langpacks, presto, refresh-packagekit  
    Adding en_US to language list  
    openssh-clients-5.5p1-21.fc14.2.i686 : An open source SSH client applications  
    Repo : fedora  
    Matched from:  
    Filename : /usr/bin/ssh  
      
    openssh-clients-5.5p1-24.fc14.2.i686 : An open source SSH client applications  
    Repo : updates  
    Matched from:  
    Filename : /usr/bin/ssh  
      
    openssh-clients-5.5p1-24.fc14.2.i686 : An open source SSH client applications  
    Repo : installed  
    Matched from:  
    Other : Provides-match: /usr/bin/ssh

You can also use rpm to find the same information.

    [root@bcane ~]# rpm -q --whatprovides /usr/bin/ssh
    openssh-clients-5.5p1-24.fc14.2.i686

One of the major differences between the two is Yum will check its repositories to find any package that can offer this binary. Where as rpm will check the rpmdb to tell you which exact package installed that binary.

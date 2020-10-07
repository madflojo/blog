---
authors:
- Benjamin Cane
categories:
- Command Line
- How To and Tutorials
- Linux
- Linux Commands
- Unix
- Unix Commands
date: '2011-08-03T03:44:00'
draft: false
header:
  caption: ''
  image: ''
tags:
- fedora
- linux
- tech
- yum
title: 'Yum: Search and Install'
url: /2011/08/03/yum-search-and-install

---

Yum is one of the easiest methods of installing packages on Red Hat and its variants. Here is a quick example of how to search and install a package.

We will be installing irssi today.

To search a package you simply use the search command.

    [root@bcane ~]# yum search irssi  
    Matched: irssi   
    irssi-devel.i686 : Development package for irssi  
    irssi-otr.i686 : Off-The-Record messaging plugin for irssi  
    irssi-xmpp.i686 : XMPP plugin into irssi  
    irssi.i686 : Modular text mode IRC client with Perl scripting  
    ctrlproxy.i686 : ctrlproxy  
    dvtm.i686 : Tiling window management for the console  
    ekg.i686 : A client compatible with Gadu-Gadu  
    purple-plugin_pack-pidgin.i686 : A set of plugins for pidgin  
    xchat-otr.i686 : Off-The-Record messaging plugin for xchat

After you found the package you want install it.

    [root@bcane ~]# yum install irssi
    Loaded plugins: langpacks, presto, refresh-packagekit  
    Adding en_US to language list  
    Setting up Install Process  
    Resolving Dependencies  
    --> Running transaction check  
    ---> Package irssi.i686 0:0.8.15-3.fc14 set to be installed  
    --> Finished Dependency Resolution  
      
    Dependencies Resolved  
      
    Installing:  
    irssi i686 0.8.15-3.fc14 fedora 779 k  
      
    Transaction Summary  
    Install 1 Package(s)  
      
    Total download size: 779 k  
    Installed size: 2.3 M  
    Is this ok [y/N]: y  
    Downloading Packages:  
    Setting up and reading Presto delta metadata  
    Processing delta metadata  
    Running rpm_check_debug  
    Running Transaction Test  
    Transaction Test Succeeded  
    Running Transaction  
    Installed:  
    Complete!

One of the best features of Yum is that it will resolve dependency issues for you and install additional packages, but only after asking nicely.

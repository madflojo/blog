---
authors:
- Benjamin Cane
categories:
- Administration
- How To and Tutorials
- Linux
- Linux Commands
date: '2011-07-08T02:08:00'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- tech
- usermod
title: 'usermod: Appending to Additional Groups'
url: /2011/07/08/usermod-appending-to-additional-groups

---

This is one of those things that I found out the hard way long long ago.

When using the usermod command in Linux to add additional groups if you want to only list the new groups the user is in you must use the -aG flags rather than a simple -G.

When specifying -G by itself you are telling usermod to change the users additional groups to the groups specified and only those groups. The user will be removed from any other group. If you use -aG then the groups mentioned are appended and not removed.

**Here are some examples:**

    [root@bcane ~]# id bcane  
    uid=500(bcane) gid=500(bcane) groups=500(bcane),100(users)

My user has a primary group of bcane and an additional group of users

    [root@bcane ~]# usermod -G wheel bcane  
    [root@bcane ~]# id bcane  
    uid=500(bcane) gid=500(bcane) groups=500(bcane),10(wheel)

My user now has a primary group of bcane and an additional group of wheel. It was removed from the users group via the usermod command.

    [root@bcane ~]# usermod -aG users bcane  
    [root@bcane ~]# id bcane  
    uid=500(bcane) gid=500(bcane) groups=500(bcane),10(wheel),100(users)

Now my user is part of both the users and wheel group because I asked usermod to append the additional groups.

    -G, --groups _GROUP1_[_,GROUP2,_[_,GROUPN_]]] 

A list of supplementary groups which the user is also a member  of. Each group is separated from the next by a comma, with no  intervening whitespace. The groups are subject to the same restrictions as the group given with the **-g** option. If the user is currently a member of a group which is not listed, the user will be removed from the group. This behavior can be changed via **-a** option, which appends user to the current supplementary group list.

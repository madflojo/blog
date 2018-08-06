---
authors:
- Benjamin Cane
categories:
- Administration
- Linux
date: '2011-07-01T02:11:00'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- tech
- unix
title: Do Symlinks use up Inodes?
url: /2011/07/01/do-symlinks-use-up-inodes

---

A question was asked today "Do Symlinks use Inodes when they are  created" I didn't know off the top of my head, so I had to go find the  answer. Rather than googling I simply used the `stat` command to answer my question. Which by the way is Yes, but hardlinks do not.

I created a file called file.real, a hardlink to that file called file.hardlink and a symlink called file.symlink.

    # stat file.*  
    ** File: `file.hardlink'**  
     Size: 0  Blocks: 0 IO Block: 4096 regular empty file  
    Device: fd00h/64768d **Inode: 23032** Links: 2  
    Access: (0664/-rw-rw-r--) Uid: ( 500/ bcane) Gid: ( 500/ bcane)  
    Access: 2011-06-30 14:55:23.032068478 -0700  
    Modify: 2011-06-30 14:55:23.032068478 -0700  
    Change: 2011-06-30 14:55:48.784938406 -0700  
    ** File: `file.real'**  
     Size: 0  Blocks: 0 IO Block: 4096 regular empty file  
    Device: fd00h/64768d **Inode: 23032** Links: 2  
    Access: (0664/-rw-rw-r--) Uid: ( 500/ bcane) Gid: ( 500/ bcane)  
    Access: 2011-06-30 14:55:23.032068478 -0700  
    Modify: 2011-06-30 14:55:23.032068478 -0700  
    Change: 2011-06-30 14:55:48.784938406 -0700  
    ** File: `file.symlink' -> `file.real'**  
     Size: 9  Blocks: 0 IO Block: 4096 symbolic link  
    Device: fd00h/64768d** Inode: 39332** Links: 1  
    Access: (0777/lrwxrwxrwx) Uid: ( 500/ bcane) Gid: ( 500/ bcane)  
    Access: 2011-06-30 14:55:50.574833081 -0700  
    Modify: 2011-06-30 14:55:31.079089339 -0700  
    Change: 2011-06-30 14:55:31.079089339 -0700

So as you can see a symlink will create a new Inode, however a hardlink will not.

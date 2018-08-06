---
authors:
- Benjamin Cane
categories:
- All Articles
- Command Line
- Linux
- Linux Commands
date: '2012-05-24T15:46:31'
draft: false
header:
  caption: ''
  image: ''
tags:
- filesystems
- hardlinks
- inode
- linux
- stat
- tech
- unix
title: 'Stat: Detailed information about a file'
url: /2012/05/24/stat-detailed-information-about-a-file

---

Stat is a command that I never knew about until somewhat recently but afterwards have had more and more reasons to use it. When run against a file stat will show detailed information about the file, this information can be extremely useful and I want to highlight some of the information I've found useful from stat.

    $ stat rsync.out
       File: `rsync.out'
       Size: 696506    	Blocks: 1368       IO Block: 4096   regular file
     Device: fc00h/64512d	Inode: 13862       <strong>Links: 1</strong>
     Access: (0644/-rw-r--r--)  Uid: ( 1000/madflojo)   Gid: ( 1000/madflojo)
     Access: 2012-05-21 19:28:00.953777255 -0700
     Modify: 2012-05-24 08:30:19.949780228 -0700
     Change: 2012-05-24 08:30:19.949780228 -0700

**Inode**

The stat command shown above displays an inode number of 13862, this is the inode number of my file. It's not often that you need an inode number but to give an example usage if you wanted to compare two files to see if they are a hardlink or not you can check if the inode number is different for each file.

**Links**

The links count is a count of how many hardlinks exist for that file. The way hardlinks work is basically by creating another access point for the same inode/file. When you have multiple links the number raises. As a note the file shown above does not have any hard links created for it hence why the links count is only 1, the original file is the only link.

**Access Time**

Access time has been extremely helpful for me in many situations, it answers questions like is it possible to modify the file without the access time changing. As seen in the example, yes. ls is able to show you the access time as well but by default with a `-l` it will only show you the change time.

I'm sure there are many other cases where stat comes in handy but for me these 3 seem to be the most common. If you know of any more common use cases post a comment and share it with us.

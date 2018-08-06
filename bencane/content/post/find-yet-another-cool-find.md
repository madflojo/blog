---
authors:
- Benjamin Cane
categories:
- All Articles
- Command Line
- Linux
- Linux Commands
- Unix
- Unix Commands
date: '2011-09-13T20:01:05'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- tech
- unix
title: 'find: Print type of file, inode #, filename and link destination'
url: /2011/09/13/find-yet-another-cool-find

---

I have been playing with find a lot lately due to some tasks I have had and someone asked me of a way to duplicate the directory, files, symlinks, and hardlinks of a very large directory on a system that is not connected in any fashion (this eliminates tar or rsync).

The files dont necessarily need to have data and they probably shouldn't in this case.

Here is the solution I gave him.

Use the find below to create a file that outputs type of file, inode number, filename, link destination if its a symlink. From there he was going to have to script recreating empty files, and creating symlinks/hardlinks to those files.

    [bcane@bcane play]$ find ./ -printf %y %i %p %lrn
    d 137042 ./
    d 145160 ./somedir
    f 135119 ./somefile
    l 145231 ./somedir1 somedir
    l 149063 ./somedir2 somedir
    l 149112 ./somedir3 somedir
    f 135119 ./somefile2

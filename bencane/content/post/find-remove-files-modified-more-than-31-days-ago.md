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
date: '2011-08-18T20:31:00'
draft: false
header:
  caption: ''
  image: ''
tags:
- find
- linux
- tech
- unix
title: 'find: Remove files modified more than 31 days ago'
url: /2011/08/18/find-remove-files-modified-more-than-31-days-ago

---

This is one of those things that you will run into eventually and once you know how, it is extremely useful.

**Example:**

    # find ./ -type f -mtime +31 -exec rm {} ;

This will find all of the files older than 31 days, If you want to do files and directories you will need two commands.

    # find ./ -not -type d -mtime +31 -exec rm {} ;  
    # find ./ -type d -mtime +31 -exec rmdir {} ;

The only reason you run the commands twice is because when find runs rm on a non empty directory it will error. This is safer than using an `rm -Rf` just in case find wants to delete a directory with newer files in it.

**Update**

I just found the below syntax while writing this, in Unix/Linux there are many ways to skin a cat.

**Example:**

     [root@bcane tmp]# find ./ -mtime +31  
     ./sudoers.new  
     ./file.symlink  
     ./somedirectory  
     ./play/list.txt2  
     ./tar.tgz  
     [root@bcane tmp]# find ./ -mtime +31 -delete  
     [root@bcane tmp]# find ./ -mtime +31

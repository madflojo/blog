---
authors:
- Benjamin Cane
categories:
- All Articles
- Command Line
- How To and Tutorials
- Linux
- Linux Commands
- Troubleshooting
- Unix
- Unix Commands
date: '2011-10-14T20:30:06'
draft: false
header:
  caption: ''
  image: ''
tags:
- gzip
- linkedin
- linux
- tech
- unix
title: 'gzip: Restoring original filename'
url: /2011/10/14/gzip-restoring-original-filename

---

I can't say this has happened to me often but recently the question came up on whether or not gzip retains the original filename.

Here are the commands necessary to not only find the original filename but uncompress the file with its original filename.

**Identifying:**

    madflojo@eee-buntu:~/Downloads$ gzip datacenter-me.jpg  
    madflojo@eee-buntu:~/Downloads$ gzip -l datacenter-me.jpg.gz  
        compressed    uncompressed ratio uncompressed_name  
        23386        23392  0.2% datacenter-me.jpg

As you can see from the above the filename is stored in the gzip file. For this exercise we are going to rename the file to match an inode number (this will come in handy if you have disk corruption).

    madflojo@eee-buntu:~/Downloads$ mv datacenter-me.jpg.gz 12345  
    madflojo@eee-buntu:~/Downloads$ gzip -l noname  
        compressed    uncompressed ratio uncompressed_name  
        23386        23392  0.2% 12345

When you rename the file and run the same command the name changes. This is because gzip will try to create a similar filename to the current filename.

    madflojo@eee-buntu:~/Downloads$ gzip --name -l 12345  
        compressed    uncompressed ratio uncompressed_name  
        23386        23392  0.2% datacenter-me.jpg

If you add the `--name` flag you will now see the original filename.

**Extracting:**

    madflojo@eee-buntu:~/Downloads$ gunzip 12345  
    gzip: 12345: unknown suffix -- ignored

As you can see gunzip will not extract the file when it does not have a known Suffix such as .gz. This is because gunzip cannot determine how to name the new uncompressed file.

    madflojo@eee-buntu:~/Downloads$ gunzip -S "" 12345  
    gzip: 12345 already exists; do you wish to overwrite (y or n)? n  
    not overwritten

If you add the -S flag you can specify the suffix, in our case it is a blank suffix. However gunzip tries to create the file with its new name.

    madflojo@eee-buntu:~/Downloads$ gunzip --name -S "" 12345  
    madflojo@eee-buntu:~/Downloads$ ls -la datacenter-me.jpg  
    -rw-r--r-- 1 madflojo madflojo 23392 2011-10-06 13:47 datacenter-me.jpg

By specifying a blank suffix and the `--name` gunzip will uncompress the file with its original filename.

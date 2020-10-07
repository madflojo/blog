---
authors:
- Benjamin Cane
categories:
- Command Line
- How To and Tutorials
- Linux
- Linux Commands
date: '2011-06-25T01:24:57'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- tech
- unix
title: sfdisk Goodies
url: /2011/06/25/sfdisk-goodies

---

Just some quickies for today.

## Copy a partition table from one disk to another

    # sfdisk -d /dev/sda | sfdisk /dev/sdb

or

    # sfdisk -d /dev/sdc > partition_table.out  
    # cat partition_table.out | sfdisk /dev/sdc

## Get the size of a disk

    # /sbin/sfdisk -s /dev/sdf

And finally the coolest part.

## Partition a disk for linux without specifying a size (making 1 big partition).

    # echo L | sfdisk /dev/sdf

You can do something similar to make multiple partitions but I'll leave that up to you and some googling.

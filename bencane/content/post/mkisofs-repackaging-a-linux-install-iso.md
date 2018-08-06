---
authors:
- Benjamin Cane
categories:
- All Articles
- Command Line
- Linux
- Linux Commands
date: '2013-06-12T12:39:19'
description: Repackaging a Linux installation DVD using mkisofs
draft: false
header:
  caption: ''
  image: ''
tags:
- all
- iso file
- isolinux
- linux
- linux os
- mkisofs
- red hat
- red hat os
title: 'mkisofs: Repackaging a Linux Install ISO'
url: /2013/06/12/mkisofs-repackaging-a-linux-install-iso

---

In the office I use Red Hat quite often and one of the quicker ways to provision a Red Hat server is via kickstart. There are many ways to reach a kickstart file during initial install (NFS, HTTP, FTP) but one of the ways I commonly use is to put the file on the installation DVD itself.

The below steps are what I use to add a custom directory to the installation iso file.

## Mount the official ISO as a directory

In order to access the contents of the ISO file we can mount it as a file system.

    # mkdir -p /mnt/linux
    # mount -o loop /tmp/linux-install.iso /mnt/linux

## Copy the contents to a working directory

Since the ISO is read-only we will need to copy the contents into another directory that we can modify and add what we want.

    # cd /mnt/
    # tar -cvf - linux | (cd /var/tmp/ && tar -xf - )

## Make your changes

At this point you can add to or modify any of the files and directories in the `/var/tmp/linux` directory.

## Repackage the directory into a new ISO file

Once finished we will repackage the directory into a new boot-able ISO file.

    # cd /var/tmp/linux
    # mkisofs -o ../your-new.iso -b isolinux/isolinux.bin -c isolinux/boot.cat 
    -no-emul-boot -boot-load-size 4 -boot-info-table -J -R -V Your Disk Name Here .

---
authors:
- Benjamin Cane
categories:
- All Articles
- Cheat Sheets
- Command Line
- Linux
- Linux Commands
- Unix
- Unix Commands
date: '2012-07-22T16:54:23'
draft: false
header:
  caption: ''
  image: ''
tags:
- apple
- debian
- exec
- executable files
- find
- gnu
- inode
- linkedin
- linux
- linux os
- mac osx
- redhat
- sudo
- suid
- suid files
- tech
- ubuntu
- unix
title: 'Cheat Sheet: 21 useful find commands'
url: /2012/07/22/cheat-sheet-21-useful-find-commands

---

For todays article I wanted to put together a quick little cheat sheet for some GNU find command examples.

Some of these commands will be basic some will be more advanced, but they all will be useful. As a caveat some commands don't work in all Unix environments and this is especially true with older releases. If you find yourself in one of those situations there is a way to make the find command work you will just need to use different methods like the `-exec` flag.

### Find things by name
     
     # find /path/to/search -name filename

**Example**
     
     # find /etc -name hosts
      /etc/hosts

### Find things by name (case-insensitive)
     
     # find /path/to/search -iname filename

**Example**
     
     # find /etc -iname HOSTS
      /etc/hosts

### Find only files by name
     
     # find /path/to/search -name filename -type f

**Example**
     
     # find /etc -name network* -type f
      /etc/init/networking.conf

### Find only directories by name
     
     # find /path/to/search -name dirname -type d

**Example**
     
     # find /etc -name network* -type d
      /etc/apparmor/init/network-interface-security

### Find all symlinks
     
     # find /path/to/search -type l

**Example**
     
     # find /etc -type l
      /etc/vtrgb

### Find things by owner
     
     # find /path/to/search -user owner

**Example**
     
     # find ./ -user root
      ./
      ./log.file

### Find executable files
     
     # find /path/to/search -type f -executable

**Example**
     
     # find ./ -type f -executable
     ./4/2651.file

### Find SUID files
     
     # find /path/to/search -perm -4000

**Example**
     
     # find /sbin -perm -4000
     /sbin/mount.ecryptfs_private

### Find things changed today
     
     # find /path/to/search -daystart -ctime -1

**Example**
     
     # find ./ -daystart -ctime -1
      ./

### Find things changed in the last 24 hours
     
     # find /path/to/search -ctime -1

**Example**
     
     # find ./ -ctime -1
      ./

### Counting how many things you find
     
     # find /path/to/search | wc -l

**Example**
     
     # find ./ | wc -l
      14674

### Deleting things you find
     
     # find /path/to/search -delete

### Deleting things you find (with xargs)
     
     # find /path/to/search | xargs rm

### Deleting things you find (with exec)
     
     # find /path/to/search -exec rm {} ;

### Printing Type of file, Filename & Inode #
     
     # find /path/to/search -printf "%y %i %prn"

**Example**
     
     # find ./ -printf "%y %i %prn"
      d 4852409 ./

### Finding Broken Symlinks
     
     # find /path/to/search -follow -lname "*"

**Example**
     
     # find ./ -follow -lname "*"
      ./bad_link

### Find files older than 31 days and delete them
     
     # find /path/to/search -mtime +31 -delete

**Example**
     
     # find ./ -mtime +31
      ./sudoers.new
      ./file.symlink
      ./somedirectory
      ./play/list.txt2
      ./tar.tgz
      # find ./ -mtime +31 -delete
      # find ./ -mtime +31

### Remove Empty Directories
     
     # find /path/to/search -type d -exec rmdir --ignore-fail-on-non-empty {} + ;

### Tar files changed today
     
     # tar -cvzf ../files_created_today.tgz `find /path/to/search -type f -daystart -ctime -1`

### Find files bigger than X Size
     
     # find /path/to/search -size +

**Example**
     
     # find ./ -size +100M
     ./madflojo/Downloads/ubuntu-12.04-server-amd64.iso

### Using Regex with find
     
     # find /path/to/search -regex 'regex pattern (full path)'

**Example**
     
     # find /var -regex '.*/tmp/.*[0-9]*.file'
     /var/tmp/testing/2/914.file

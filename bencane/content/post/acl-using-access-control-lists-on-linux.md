---
authors:
- Benjamin Cane
categories:
- Administration
- How To and Tutorials
- Linux
- Security
date: '2012-05-27T21:00:33'
description: A tutorial showing how to enable Linux Access Control Lists as well as
  how to use ACL's to go beyond basic permissions
draft: false
header:
  caption: ''
  image: ''
tags:
- acl
- debian
- filesystems
- kernel
- linkedin
- linux
- linux os
- permissions
- redhat
- tech
- ubuntu
- unix
title: 'ACL: Using Access Control Lists on Linux'
url: /2012/05/27/acl-using-access-control-lists-on-linux

---

Access Control Lists aka ACL's are one of those obscure Linux tools that isn't used every day; and if you find yourself using ACL's every day than you probably have a very complicated Linux environment.

A few years ago I had an engineer tell me "Any thing you want to solve with ACL's can be solved with standard unix permissions" and while he may have just been justifying why he didn't know ACL's very well. He did have a point; kind of.

In general ACL's are a bit of an advanced topic for Unix/Linux systems administrators and unless you have a shop full of experienced sysadmins and users than it is usually best to reserve ACL's for when there is no better option. With that said, I have found several occasions where ACL's were needed and it is always a good idea to learn advanced topics even if they aren't used in everyday situations.

This article can be used as a tutorial for ACL's on Linux; I will be covering the basics of ACL's and give some examples of usage.

## Prerequisites

### Filesystem options

Before using ACL's we must first verify that our filesystem has the acl option enabled.

A common way to enable acl support on a filesystem is to add the `acl` option to a filesystems mount options in `/etc/fstab`. We can check if that has been done on this system by using the mount command.
     
```shell
root@testvm:~# mount | grep root
/dev/mapper/workstation-root on / type ext4 (rw,errors=remount-ro)
```

In this case the acl option has not been added but that doesn't mean our filesystem doesn't have acl's enabled. On most distributions the default filesystems have the acl option as part of the default mount options. You can check if your filesystems have acl as part of the defaults by using the `tune2fs` command.
     
```shell
root@testvm:~# tune2fs -l /dev/mapper/workstation-root
tune2fs 1.42 (29-Nov-2011)
Filesystem volume name:   <none>
Last mounted on:          /
Filesystem UUID:          f558402c-a418-4892-87e2-071c1a85898c
Filesystem magic number:  0xEF53
Filesystem revision #:    1 (dynamic)
Filesystem features:      has_journal ext_attr resize_inode dir_index filetype needs_recovery extent flex_bg sparse_super large_file huge_file uninit_bg dir_nlink extra_isize
Filesystem flags:         signed_directory_hash
Default mount options:    user_xattr acl
```

As you can see on my test system the default mount options contain acl, in this case my filesystem will support acl's even if I don't specify it during the mount process. If your filesystem does not have acl as a default mount option, than you can add it during the mount process easily by editing the fstab file.
     
```shell
root@testvm:~# vi /etc/fstab
```

Simply add the term `acl` to the mount options as shown below.

**Before:**
     
```
/dev/mapper/workstation-root /               ext4    errors=remount-ro 0       1
```

**After:**
     
```
/dev/mapper/workstation-root /               ext4    acl,errors=remount-ro 0       1
```

Once your fstab file is edited you can remount your filesystem with the mount command.
     
```shell
root@testvm:~# mount -o remount /
root@testvm:~# mount | grep root
/dev/mapper/workstation-root on / type ext4 (rw,acl,errors=remount-ro)
```

### ACL Utilities

Now that your filesystem supports acl's we must make sure that you have the acl utilities installed. My test machine is an Ubuntu server install so I will use the `dpkg` command, if you are running a different Linux distro than you may need to use another package manager, consult your distro's documentation.
     
```shell
root@testvm:~# dpkg --list | grep acl
ii  libacl1                          2.2.51-5ubuntu1            Access control list shared library
```

As you can see on my test machine I have the libraries necessary for acl support but not the command line utilities to interact with acl's. Lets change that by installing the tools with `apt-get`; again this is part is dependent on the distribution you are using.
     
```shell
root@testvm:~# apt-get install acl
```

Now we check again, and it is installed.
     
```shell
root@testvm:~# dpkg --list | grep acl
ii  acl                              2.2.51-5ubuntu1            Access control list utilities
ii  libacl1                          2.2.51-5ubuntu1            Access control list shared library
```

## Setting and listing acl's with getfacl and setfacl

Now that we have the utilities installed we can start using the `setfacl` and `getfacl` commands.

### Setting ACL's with setfacl

The `setfacl` command is used to set acl lists on files and directories, `setfacl` is the acl version of the `chmod` command.

As an example I am going to give the testusers group permission to read from the appdir which is owned by root:appgroup.
     
```shell
root@testvm:/var/tmp# ls -la | grep appdir
drwxrwxr-x  2 root appgroup 4096 May 27 10:45 appdir
```

To add these permissions we will use the `setfacl` command
     
```shell
root@testvm:/var/tmp# setfacl -m g:testusers:r appdir/
```

Let's break the command down a little bit.

```shell
-m
```

The `-m` option tells setfacl to modify the acl list for the specified directory.

```shell
g:testusers:r
```

This is actually the access control list that is being set. The first column is specifying `g` for group, the second column is the group name that I want the permissions to be set for and the last column is the permissions I want that group to have. In this case the read permission.

```shell
appdir/
```

This is the directory that I am setting the permissions on.

### Checking the ACL list with getfacl

Once you've set the acl with setfacl it is common sense to check if it took effect, in order to do so you will need to use the `getfacl` command.
     
```shell
root@testvm:/var/tmp# getfacl appdir/
# file: appdir/
# owner: root
# group: appgroup
user::rwx
group::rwx
group:testusers:r--
mask::rwx
other::r-x
```

The output of `getfacl` is pretty self explanatory, you can see the rule that we added below the standard group entry.

### Identifying files/directories that have ACL's

While the standard unix permissions are displayed with the `ls -l` command; the defined ACL's are a little more verbose and are not a part of the long listing. The command `ls` will tell you if a file or directory does have acl's, it's just not that obvious.
     
```shell
root@testvm:/var/tmp# ls -la | grep appdir
drwxrwxr-x+  2 root appgroup 4096 May 27 10:45 appdir
```

As you can see there is now a `+` at the end of the directories permissions. This `+` is the indicator that this file or directory has acl's, from here you can use the `getfacl` command to see what they are.

## Examples of Usage

Now that we have a filesystem that supports ACL's and we know how to set and review the ACL's lets run through a few examples of ACL usage.

### Use Cases
	
  * Removing all acl entries from a file or directory
  * Set test users to have read access to all files in a directory
  * Set the same acl changes recursively
  * Set the same acls on all newly created files automatically
  * Set testuser1 to have read, write and execute access to the appuser1 directory
  * Set all users to have read, write and execute access to the shared directory
  * Remove the acl for testuser1 on appuser1 directory

#### Removing all acl entries from a file or directory

Before we start messing with acl's in my directory I want to clear out all of the acl's it previously had. Doing this one by one can be a bit of a pain, its a good thing the setfacl command gives you the ability to remove all acl's on a specified file or directory. This can be accomplished using the `-b` option of setfacl.
   
```shell  
root@testvm:/var/tmp# getfacl appdir/
# file: appdir/
# owner: root
# group: appgroup
user::rwx
group::rwx
group:testusers:r--
mask::rwx
other::r-x
     
root@testvm:/var/tmp# setfacl -b appdir/
root@testvm:/var/tmp# getfacl appdir/
# file: appdir/
# owner: root
# group: appgroup
user::rwx
group::rwx
other::r-x
```

Keep in mind when using the `-b` option that this will remove all of the acl rules on the specified directory.

#### Set testusers to have read access to all files in the appdir directory

This is a pretty basic acl, we want the testusers group to have read access to all files in the appdir directory.
     
```shell
root@testvm:/var/tmp# setfacl -m g:testusers:r appdir/
root@testvm:/var/tmp# getfacl appdir
# file: appdir
# owner: root
# group: appgroup
user::rwx
group::rwx
group:testusers:r-- mask::rwx
other::r-x
```

#### Set the changes recursively

The appdir has 2 sub directories appdir/appuser1 and appdir/appuser2 in this case we want the acl rules set above to apply to these directories as well. This can easily be accomplished by adding the `-R` (recursive) option in `setfacl`. This works exactly like the recursive option for chmod.
     
```shell
root@testvm:/var/tmp# setfacl -Rm g:testusers:r appdir/
root@testvm:/var/tmp# getfacl appdir/*
# file: appdir/appuser1
# owner: appuser1
# group: appgroup
user::rwx
group::r-x
group:testusers:r-- mask::r-x
other::r-x
     
# file: appdir/appuser2
# owner: appuser2
# group: appgroup
user::rwx
group::r-x
group:testusers:r-- mask::r-x
other::r-x
```

#### Set the same acl's on all newly created files automatically

The `-d` (default) option in `setfacl` is extremely useful; this option will allow us to set an acl rule to be the default rule. When this is set on a directory this makes all new files or directories created within that directory inherit the same acl rules.
     
```shell
root@testvm:/var/tmp# setfacl -dm g:testusers:r appdir/
root@testvm:/var/tmp# touch appdir/file1
root@testvm:/var/tmp# mkdir appdir/dir1
root@testvm:/var/tmp# getfacl appdir/*
# file: appdir/appuser1
# owner: appuser1
# group: appgroup
user::rwx
group::r-x
group:testusers:r--
mask::r-x
other::r-x
     
# file: appdir/appuser2
# owner: appuser2
# group: appgroup
user::rwx
group::r-x
group:testusers:r--
mask::r-x
other::r-x
     
# file: appdir/dir1
# owner: root
# group: root
user::rwx
group::rwx
group:testusers:r-- mask::rwx
other::r-x
default:user::rwx
default:group::rwx
default:group:testusers:r-- default:mask::rwx
default:other::r-x
     
# file: appdir/file1
# owner: root
# group: root
user::rw-
group::rwx			#effective:rw-
group:testusers:r-- mask::rw-
other::r--
```

As you can see dir1 also have the default acl rules as appdir, yet appuser1 does not. This is because we did not set the default recursively; this can be done by using the `-R` option.
     
```shell
root@testvm:/var/tmp# setfacl -Rdm g:testusers:r appdir/
root@testvm:/var/tmp# getfacl appdir/appuser1
# file: appdir/appuser1
# owner: appuser1
# group: appgroup
user::rwx
group::r-x
group:testusers:r--
mask::r-x
other::r-x
default:user::rwx
default:group::r-x
default:group:testusers:r--
default:mask::r-x
default:other::r-x
```

#### Set testuser1 to have read, write and execute access to the appuser1 directory

While the user testuser1 is in the testusers group and has read access to the appuser1 directory he does not have write access. In this case we want to give him write access without giving the rest of the testusers write access. This can be done using acl's by specifying a specific user rather than a group.
     
```shell
root@testvm:/var/tmp# setfacl -m u:testuser1:rwx appdir/
root@testvm:/var/tmp# getfacl appdir/
# file: appdir/
# owner: root
# group: appgroup
user::rwx
user:testuser1:rwx group::rwx
group:testusers:r--
mask::rwx
other::r-x
default:user::rwx
default:group::rwx
default:group:testusers:r--
default:mask::rwx
default:other::r-x
```

The user testuser1 can now create files in the appdir1 directory.
     
```shell
root@testvm:/var/tmp# sudo -u testuser1 touch appdir/file2
root@testvm:/var/tmp# ls -la appdir/file2
-rw-rw-r--+ 1 testuser1 testusers 0 May 27 12:17 appdir/file2
```

#### Set all users to have read, write and execute to the shared directory

We have now given users and groups permissions on directories and files, but what happens when we want all users to have access to a directory? Adding every users name or group could get tedious, in this case we can set the "other" or "world" permissions so that all users on a system can access this directory.
     
```shell
root@testvm:/var/tmp# setfacl -m o::rwx shared
root@testvm:/var/tmp# getfacl shared/
# file: shared/
# owner: root
# group: root
user::rwx
group::r-x
other::rwx
```

You might be asking yourself right now "wait a minute, did setfacl just set the permissions to 757?"; why yes it did! ACL's are just an extension of the standard unix permissions, in this case because we are not specifying a user or group; setfacl will simply just change the mode of the file. Tricky, yes I know.

#### Remove the acl for testuser1 on appuser1 directory

Unlike the `-b` option that removes all acl's on a directory or file the `-x` option will only remove the specified rule. This is useful for when you maybe fat fingered an acl rule and don't want to completely remove all of the acl rules attached to that file/directory.
     
```shell
root@testvm:/var/tmp# setfacl -x u:testuser1 appdir/
root@testvm:/var/tmp# getfacl appdir/
# file: appdir/
# owner: root
# group: appgroup
user::rwx
group::rwx
group:testusers:r--
mask::rwx
other::r-x
default:user::rwx
default:group::rwx
default:group:testusers:r--
default:mask::rwx
default:other::r-x
```

As you can see setfacl did not remove the group permissions or the default permissions only the acl specified.

## Closing Thoughts

By now if you have followed this primer you should have a general idea of how ACL's work with Linux and the commands you need to set and review them. I do want to give a word of advice however; If you find yourself wanting to use ACL's to solve a problem, don't. That is unless you work in a shop where all of the sysadmins and users are experienced Linux users and understand how ACL's work and how to troubleshoot permissions problems with ACL's. If thats the case then go for it and have fun.

For the most part, most sysadmin's don't use ACL's everyday like they would normal Unix permissions. With that said if you are the only person who will admin the system and you want to learn and use ACL's, go for it! You can only blame yourself if it all goes wrong.

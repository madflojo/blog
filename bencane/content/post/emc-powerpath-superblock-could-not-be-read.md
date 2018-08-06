---
authors:
- Benjamin Cane
categories:
- All Articles
- Linux
- Red Hat
- Troubleshooting
date: '2013-06-05T01:55:38'
description: How to get around a simple setup issue where fsck tries to check a SAN
  disk before EMC PowerPath starts
draft: false
header:
  caption: ''
  image: ''
tags:
- emc powerpath
- filesystems
- fsck
- linux os
- red hat
- red hat os
- superblock
title: 'EMC PowerPath: superblock could not be read'
url: /2013/06/05/emc-powerpath-superblock-could-not-be-read

---

Recently while working on a system that uses EMC PowerPath, I ran into a little issue after rebooting.

## The Issue

    fsck.ext3: No such file or directory while trying to open /dev/emcpowera1
    /dev/emcpowera1:
    The superblock could not be read or does not describe a correct ext2 filesystem.

## The Cause

The root cause of this issue is pretty simple when a Linux system boots it performs file system checks on file systems listed within the `/etc/fstab` file. When my system reached the `/boot` file system which has a device of `/dev/emcpowera1`, it could not find that device. Therefore the system could not perform a check and went into maintenance mode.

The reason `/dev/emcpowera1` is not found is because PowerPath has not started yet. When a Red Hat based system is booting after the init process is spawned it will execute the `/etc/rc.sysinit` script. Within that file are the commands to both start PowerPath and run a file system check on all of the file systems listed in `/etc/fstab`.

    # grep Power rc.sysinit
    # Configure and initialize PowerPath.
    if [ -f /etc/init.d/PowerPath ]; then
    /etc/init.d/PowerPath start

Unfortunately the snippet that starts PowerPath is listed after the file system checks are initiated.

## The Fix

The resolution for this problem is simple; disable boot time file system checks on anything that references an EMC PowerPath device. To do this I will edit the `/etc/fstab` and change the `passno` field to 0

    # vi /etc/fstab

**Find:**

    #device mount_point fstype options dump_freq passno
    /dev/emcpowera1 /boot ext3 defaults 1 2

**Modify To:**

    #device mount_point fstype options dump_freq passno
    /dev/emcpowera1 /boot ext3 defaults 0 0

Now the next time the system boots it will skip the `/boot` file system check and boot without any errors.

**As a note:** I also changed the `dump_freq` to 0 on my system not because I had to for file system checks but because in my environment I will not need any dump backups of the file system.

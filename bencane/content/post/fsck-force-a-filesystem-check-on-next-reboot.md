---
authors:
- Benjamin Cane
categories:
- Administration
- All Articles
- How To and Tutorials
- Linux
date: '2011-09-06T20:02:06'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- tech
- unix
title: 'fsck: Force a filesystem check on next reboot'
url: /2011/09/06/fsck-force-a-filesystem-check-on-next-reboot

---

I haven't had to use this too often but I've had a few occasions where I had to troubleshoot timing issues in the boot process. Mainly where a service tries to start before the disks are available. We suspected that an fsck was stopping the filesystem from being mounted but the service was started anyways.

In order to test our theories we had to force a fsck on reboot.

**Example:**

    # touch /forcefsck

---
author: bencane
comments: true
date: 2011-09-06 20:02:06+00:00
popularity: None
slug: fsck-force-a-filesystem-check-on-next-reboot
title: 'fsck: Force a filesystem check on next reboot'
post_id: 47
categories:
- Administration
- All Articles
- How To &amp; Tutorials
- Linux
tags:
- linux
- tech
- unix
---

I haven't had to use this too often but I've had a few occasions where I had to troubleshoot timing issues in the boot process. Mainly where a service tries to start before the disks are available. We suspected that an fsck was stopping the filesystem from being mounted but the service was started anyways.

In order to test our theories we had to force a fsck on reboot.

**Example:**

    # touch /forcefsck


I haven't had to use this too often but I've had a few occasions where I had to troubleshoot timing issues in the boot process. Mainly where a service tries to start before the disks are available. We suspected that an fsck was stopping the filesystem from being mounted but the service was started anyways.

In order to test our theories we had to force a fsck on reboot.

**Example:**

    # touch /forcefsck

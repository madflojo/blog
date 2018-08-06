---
authors:
- Benjamin Cane
categories:
- Administration
- How To and Tutorials
- Linux
- Linux Commands
date: '2011-12-19T18:30:24'
description: Simple walkthrough on how to create a new Linux filesystem using LVM,
  fdisk and mkfs
draft: false
header:
  caption: ''
  image: ''
tags:
- fdisk
- linkedin
- linux
- lvm
- mkfs
- tech
title: Creating a new filesystem with fdisk, lvm, and mkfs
url: /2011/12/19/creating-a-new-filesystem-with-fdisk-lvm-and-mkfs

---

## **Our Task:** Create a new 10GB filesystem to store a package repository for yum


**Challenges:** The existing hard drive has been fully allocated using LVM.

**Solution:**
	
  * Add a new hard drive to the server (virtual server in this case)
	
  * Partition the drive and add it to the main logical volume
	
  * Create a new filesystem

This article assumes that by now you have physically added the hard drive to the server. In my case I am using a virtual server but the tasks are essentially the same.

### Partition the new disk drive

Before starting I will verify there are no partitions on the new disk.
     
     [root@fedora-test ~]# fdisk -l /dev/sdb 
     Disk /dev/sdb: 21.5 GB, 21474836480 bytes
     255 heads, 63 sectors/track, 2610 cylinders, total 41943040 sectors
     Units = sectors of 1 * 512 = 512 bytes
     Sector size (logical/physical): 512 bytes / 512 bytes
     I/O size (minimum/optimal): 512 bytes / 512 bytes
     Disk identifier: 0x00000000
     Disk /dev/sdb doesn't contain a valid partition table

Since there are no partitions it is safe to proceed. I will now create one big partition as I plan to add this disk to LVM and use LVM to divvy up my disk space.
     
     [root@fedora-test ~]# fdisk /dev/sdb
     Device contains neither a valid DOS partition table, nor Sun, SGI or OSF disklabel
     Building a new DOS disklabel with disk identifier 0xe1410716.
     Changes will remain in memory only, until you decide to write them.
     After that, of course, the previous content won't be recoverable.
     
     Warning: invalid flag 0x0000 of partition table 4 will be corrected by w(rite)
     
     Command (m for help): n
     Partition type:
        p   primary (0 primary, 0 extended, 4 free)
        e   extended
     Select (default p): p
     Partition number (1-4, default 1):
     Using default value 1
     First sector (2048-41943039, default 2048):
     Using default value 2048
     Last sector, +sectors or +size{K,M,G} (2048-41943039, default 41943039):
     Using default value 41943039

     
     Command (m for help): p
     Disk /dev/sdb: 21.5 GB, 21474836480 bytes
     255 heads, 63 sectors/track, 2610 cylinders, total 41943040 sectors
     Units = sectors of 1 * 512 = 512 bytes
     Sector size (logical/physical): 512 bytes / 512 bytes
     I/O size (minimum/optimal): 512 bytes / 512 bytes
     Disk identifier: 0xe1410716
     
        Device Boot      Start         End      Blocks   Id  System
     /dev/sdb1            2048    41943039    20970496   83  Linux
     
     Command (m for help): w
     The partition table has been altered!
     Calling ioctl() to re-read partition table.
     Syncing disks.

Once you type w the changes are written to disk.

### Add the partition to the volume group

My volume group name is vg_fedoratest and I will now add the new partition to that volume group with the vgextend command. This adds the additional partition space to the volume group for lvm to use.

     [root@fedora-test ~]# ls -la /dev/sdb*
     brw-rw----. 1 root disk 8, 16 Dec  6 15:08 /dev/sdb
     brw-rw----. 1 root disk 8, 17 Dec  6 15:08 /dev/sdb1

     [root@fedora-test ~]# pvcreate /dev/sdb1

     [root@fedora-test ~]# vgextend vg_fedoratest /dev/sdb1
       No physical volume label read from /dev/sdb1
       Writing physical volume data to disk "/dev/sdb1"
       Physical volume "/dev/sdb1" successfully created
       Volume group "vg_fedoratest" successfully extended

     [root@fedora-test ~]# vgdisplay vg_fedoratest
       --- Volume group ---
       VG Name               vg_fedoratest
       System ID
       Format                lvm2
       Metadata Areas        2
       Metadata Sequence No  4
       VG Access             read/write
       VG Status             resizable
       MAX LV                0
       Cur LV                2
       Open LV               2
       Max PV                0
       Cur PV                2
       Act PV                2
       VG Size               40.69 GiB
       PE Size               32.00 MiB
       Total PE              1302
       Alloc PE / Size       663 / 20.72 GiB
       Free  PE / Size       639 / 19.97 GiB
       VG UUID               0gvY4O-I3tT-WKK0-ClU2-sXDz-Nq0c-eExZz2

### Create a logical volume & filesystem

I am first using lvcreate to create the logical volume, after verifying that the logical volume created correctly I will create a new filesystem on top with mkfs.
     
     [root@fedora-test ~]# lvcreate -L 10GB -n lv_yumrepo vg_fedoratest
       Logical volume "lv_yumrepo" created

     [root@fedora-test ~]# lvdisplay vg_fedoratest/lv_yumrepo
       --- Logical volume ---
       LV Name                /dev/vg_fedoratest/lv_yumrepo
       VG Name                vg_fedoratest
       LV UUID                rpl7q1-oi6N-nZot-bjPT-Y1qi-2W28-xlBg6Q
       LV Write Access        read/write
       LV Status              available
       # open                 0
       LV Size                10.00 GiB
       Current LE             320
       Segments               1
       Allocation             inherit
       Read ahead sectors     auto
       - currently set to     256
       Block device           253:2

     [root@fedora-test ~]# mkfs -t ext3 /dev/vg_fedoratest/lv_yumrepo
     mke2fs 1.41.14 (22-Dec-2010)
     Filesystem label=
     OS type: Linux
     Block size=4096 (log=2)
     Fragment size=4096 (log=2)
     Stride=0 blocks, Stripe width=0 blocks
     655360 inodes, 2621440 blocks
     131072 blocks (5.00%) reserved for the super user
     First data block=0
     Maximum filesystem blocks=2684354560
     80 block groups
     32768 blocks per group, 32768 fragments per group
     8192 inodes per group
     Superblock backups stored on blocks:
     	32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632
     
     Writing inode tables: done
     Creating journal (32768 blocks): done
     Writing superblocks and filesystem accounting information: done
     
     This filesystem will be automatically checked every 28 mounts or
     180 days, whichever comes first.  Use tune2fs -c or -i to override.

### Mount the filesystem

Now that my filesystem is created I need to mount it; but before then I need to create the directory that the mount point will overlay and add the appropriate lines to the `/etc/fstab` file.

     [root@fedora-test ~]# mkdir /var/repo
     [root@fedora-test ~]# vi /etc/fstab
         ## Append to bottom
         /dev/mapper/vg_fedoratest-lv_yumrepo /var/repo ext3 defaults 0 0

     [root@fedora-test ~]# mount
     /dev/mapper/vg_fedoratest-lv_yumrepo on /var/repo type ext3 (rw,relatime,seclabel,user_xattr,acl,barrier=1,nodelalloc,data=ordered)


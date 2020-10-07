---
authors:
- Benjamin Cane
categories:
- Administration
- How To and Tutorials
- Linux
- Linux Commands
date: '2011-07-06T01:20:30'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- mdadm
- tech
- unix
title: 'mdadm: Manually fail a drive'
url: /2011/07/06/mdadm-manually-fail-a-drive

---

Just a quicky reference on removing a drive for those of you using mdadm.  
  
## Check the status of a raid device

    [root@bcane ~]# mdadm --detail /dev/md10  
    /dev/md10:  
     Version : 1.2  
     Creation Time : Sat Jul 2 13:56:38 2011  
     Raid Level : raid1  
     Array Size : 26212280 (25.00 GiB 26.84 GB)  
     Used Dev Size : 26212280 (25.00 GiB 26.84 GB)  
     Raid Devices : 2  
     Total Devices : 2  
     Persistence : Superblock is persistent  
      
     Update Time : Sat Jul 2 13:56:47 2011  
     State : clean, resyncing  
    Active Devices : 2  
    Working Devices : 2  
    Failed Devices : 0  
     Spare Devices : 0  
      
    Rebuild Status : 10% complete  
      
     Name : bcane.virtuals.local:10 (local to host bcane.virtuals.local)  
     UUID : 10a96ed5:92dc48e6:04b2bf43:3539e089  
     Events : 1  
      
     Number Major Minor RaidDevice State  
     0 8 33 0 active sync /dev/sdc1  
     1 8 49 1 active sync /dev/sdd1

In order to remove a drive it must first be marked as faulty. A drive can be marked as faulty either through a failure or if you want to manually mark a drive as faulty you can use the -f/--fail flag.

    [root@bcane ~]# mdadm /dev/md10 -f /dev/sdc1
    mdadm: set /dev/sdc1 faulty in /dev/md10  

    [root@bcane ~]# mdadm --detail /dev/md10
    /dev/md10:  
     Version : 1.2  
     Creation Time : Sat Jul 2 13:56:38 2011  
     Raid Level : raid1  
     Array Size : 26212280 (25.00 GiB 26.84 GB)  
     Used Dev Size : 26212280 (25.00 GiB 26.84 GB)  
     Raid Devices : 2  
     Total Devices : 2  
     Persistence : Superblock is persistent  
      
     Update Time : Sat Jul 2 14:00:18 2011  
     State : active, degraded  
    Active Devices : 1  
    Working Devices : 1  
    Failed Devices : 1  
     Spare Devices : 0  
      
     Name : bcane.virtuals.local:10 (local to host bcane.virtuals.local)  
     UUID : 10a96ed5:92dc48e6:04b2bf43:3539e089  
     Events : 19  
      
     Number Major Minor RaidDevice State  
     0 0 0 0 removed  
     1 8 49 1 active sync /dev/sdd1  
      
     0 8 33 - faulty spare /dev/sdc1

Now that the drive is marked as failed/faulty you can remove it using the -r/--remove flag.

    [root@bcane ~]# mdadm /dev/md10 -r /dev/sdc1
    mdadm: hot removed /dev/sdc1 from /dev/md10  

    [root@bcane ~]# mdadm --detail /dev/md10
    /dev/md10:  
     Version : 1.2  
     Creation Time : Sat Jul 2 13:56:38 2011  
     Raid Level : raid1  
     Array Size : 26212280 (25.00 GiB 26.84 GB)  
     Used Dev Size : 26212280 (25.00 GiB 26.84 GB)  
     Raid Devices : 2  
     Total Devices : 1  
     Persistence : Superblock is persistent  
      
     Update Time : Sat Jul 2 14:02:04 2011  
     State : active, degraded  
    Active Devices : 1  
    Working Devices : 1  
    Failed Devices : 0  
     Spare Devices : 0  
      
     Name : bcane.virtuals.local:10 (local to host bcane.virtuals.local)  
     UUID : 10a96ed5:92dc48e6:04b2bf43:3539e089  
     Events : 20  
      
     Number Major Minor RaidDevice State  
     0 0 0 0 removed  
     1 8 49 1 active sync /dev/sdd1

If you want to re-add the device you can do so with the -a flag.

    [root@bcane ~]# mdadm /dev/md10 -a /dev/sdc1
    mdadm: re-added /dev/sdc1  

    [root@bcane ~]# mdadm --detail /dev/md10
    /dev/md10:  
     Version : 1.2  
     Creation Time : Sat Jul 2 13:56:38 2011  
     Raid Level : raid1  
     Array Size : 26212280 (25.00 GiB 26.84 GB)  
     Used Dev Size : 26212280 (25.00 GiB 26.84 GB)  
     Raid Devices : 2  
     Total Devices : 2  
     Persistence : Superblock is persistent  
      
     Update Time : Sat Jul 2 18:02:21 2011  
     State : clean, degraded, recovering  
    Active Devices : 1  
    Working Devices : 2  
    Failed Devices : 0  
     Spare Devices : 1  
      
    Rebuild Status : 4% complete  
      
     Name : bcane.virtuals.local:10 (local to host bcane.virtuals.local)  
     UUID : 10a96ed5:92dc48e6:04b2bf43:3539e089  
     Events : 23  
      
     Number Major Minor RaidDevice State  
     0 8 33 0 spare rebuilding /dev/sdc1  
     1 8 49 1 active sync /dev/sdd1

One thing to keep an eye out for is that you need to specify the raid device when running these commands. If they are performed without specifying the raid device the flags take on a new meaning.

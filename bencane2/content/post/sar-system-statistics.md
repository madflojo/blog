---
authors:
- Benjamin Cane
categories:
- Command Line
- Linux
- Linux Commands
date: '2011-08-12T20:30:06'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- sar
- tech
title: 'sar: System statistics'
url: /2011/08/12/sar-system-statistics

---

Sar is a utility that will grab cpu, disk i/o, memory, and network statistics on a 10 minute interval. Sar is great for grabbing system statistics quickly; I use sar whenever I'm doing any kind of performance tuning or troubleshooting.

To use sar all you need to do is install the **sysstat** package. The package will install a cron in `/etc/cron.d` that will kick off a sar capture every 10 minutes. If you want you can change this to every 5 minutes by modifying the crontab.

Sar will even keep a months worth of data in `/var/log/sa/saXX` where XX represents the day of month.

**Example: **

    [root@bcane tmp]# sar  
    Linux 2.6.35.13-92.fc14.i686 (bcane.virtuals.local)  08/08/2011  _i686_ (1 CPU)  
      
    09:05:01 AM CPU %user %nice %system %iowait %steal %idle  
    09:10:01 AM all 0.10 0.00 0.13 0.15 0.00 99.61  
    09:15:02 AM all 0.29 6.90 1.59 14.22 0.00 77.01  
    09:20:01 AM all 0.02 0.00 0.10 0.14 0.00 99.74  
    09:25:01 AM all 0.02 0.00 0.10 0.03 0.00 99.86  
    09:30:01 AM all 0.02 0.09 1.13 12.63 0.00 86.12  
    09:35:01 AM all 0.02 0.00 0.13 0.46 0.00 99.39  
    09:40:01 AM all 0.02 0.00 0.14 0.57 0.00 99.27

To read a specific days file you can specify it with the -f option.

    [root@bcane tmp]# sar -f /var/log/sa/sa08  
    Linux 2.6.35.13-92.fc14.i686 (bcane.virtuals.local)  08/08/2011  _i686_ (1 CPU)  
      
    09:05:01 AM CPU %user %nice %system %iowait %steal %idle  
    09:10:01 AM all 0.10 0.00 0.13 0.15 0.00 99.61  
    09:15:02 AM all 0.29 6.90 1.59 14.22 0.00 77.01  
    09:20:01 AM all 0.02 0.00 0.10 0.14 0.00 99.74  
    09:25:01 AM all 0.02 0.00 0.10 0.03 0.00 99.86  
    09:30:01 AM all 0.02 0.09 1.13 12.63 0.00 86.12  
    09:35:01 AM all 0.02 0.00 0.13 0.46 0.00 99.39  
    09:40:01 AM all 0.02 0.00 0.14 0.57 0.00 99.27  

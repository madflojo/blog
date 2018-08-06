---
authors:
- Benjamin Cane
categories:
- Command Line
- How To and Tutorials
- Linux
- Linux Commands
date: '2011-08-28T20:31:05'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- tech
- unix
title: 'Top: Show CPU Usage on all cores'
url: /2011/08/28/top-show-cpu-usage-on-all-cores

---

By default the command top will show you an aggregation of the cpu  usage. If you want to see the statistics on each core you can do this within top.

**Normal top output:**

    top - 16:39:08 up 23 days, 22:03, 2 users, load average: 0.07, 0.02, 0.00  
    Tasks: 88 total, 1 running, 87 sleeping, 0 stopped, 0 zombie  
    Cpu(s): 0.0%us, 0.0%sy, 0.0%ni,100.0%id, 0.0%wa, 0.0%hi, 0.0%si, 0.0%st  
    Mem: 536684k total, 514528k used, 22156k free, 3976k buffers  
    Swap: 1048568k total, 352996k used, 695572k free, 53052k cached

After running top you can hit the **1** key and it will show you all of the cpus individually

    top - 16:44:23 up 23 days, 22:09, 2 users, load average: 0.00, 0.00, 0.00  
    Tasks: 86 total, 1 running, 85 sleeping, 0 stopped, 0 zombie  
    Cpu0 : 0.0%us, 0.0%sy, 0.0%ni,100.0%id, 0.0%wa, 0.0%hi, 0.0%si, 0.0%st  
    Cpu1 : 0.0%us, 0.0%sy, 0.0%ni,100.0%id, 0.0%wa, 0.0%hi, 0.0%si, 0.0%st  
    Cpu2 : 0.0%us, 0.0%sy, 0.0%ni,100.0%id, 0.0%wa, 0.0%hi, 0.0%si, 0.0%st  
    Cpu3 : 0.0%us, 0.0%sy, 0.0%ni,100.0%id, 0.0%wa, 0.0%hi, 0.0%si, 0.0%st  
    Mem: 536684k total, 528108k used, 8576k free, 3944k buffers  
    Swap: 1048568k total, 353760k used, 694808k free, 49552k cached

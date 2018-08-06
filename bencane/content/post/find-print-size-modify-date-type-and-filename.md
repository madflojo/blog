---
authors:
- Benjamin Cane
categories:
- Command Line
- Linux
- Linux Commands
- Unix
- Unix Commands
date: '2011-08-15T20:30:00'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- tech
- unix
title: 'Find: Print Size, Modify Date, Type, and Filename'
url: /2011/08/15/find-print-size-modify-date-type-and-filename

---

I've been running some serious finds over the past few days and found this cool method of printing the Size, Modify Date, Type (directory, link, file, ext..) and Filename. For my purposes this was pretty useful.

**Example:**

    [bcane@bcane ~]$ find ./ -printf "%s %TD %y %prn" | head  
    4096 08/14/11 d ./  
    4096 12/21/10 d ./.pulse  
    23 12/21/10 l ./.pulse/8c85d3ca772930c75bea9f640000000f-runtime  
    73728 02/11/11 f ./.pulse/8c85d3ca772930c75bea9f640000000f-stream-volumes.tdb  
    42 08/14/11 f ./.pulse/8c85d3ca772930c75bea9f640000000f-default-source  
    61440 02/11/11 f ./.pulse/8c85d3ca772930c75bea9f640000000f-device-volumes.tdb  
    43 08/14/11 f ./.pulse/8c85d3ca772930c75bea9f640000000f-default-sink  
    696 12/21/10 f ./.pulse/8c85d3ca772930c75bea9f640000000f-card-database.tdb  
    4096 12/22/10 d ./.mozilla

You can redirect this output to a file and do some helpful greps to find things like how many files you have or how many links you have without having to run multiple finds.

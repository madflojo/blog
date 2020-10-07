---
authors:
- Benjamin Cane
categories:
- How To and Tutorials
- Linux Performance Tuning
- System Monitoring
- Linux
- Linux Commands
date: '2012-07-08T00:22:24'
description: Tutorial on installing the sysstat package and using sar to identify
  performance statistics
draft: false
header:
  caption: ''
  image: ''
tags:
- cpu
- cpuinfo
- cronjob
- i/o
- iostat
- linkedin
- linux
- linux os
- mpstat
- network
- performance monitoring
- sadf
- sar
- sar command
- sar system
- swap
- sysstat
- sysstat package
- system activity reporter
- system statistics
- systems performance
- unix
- unix tools
title: 'Sar & Sysstat: Linux Performance Statistics with Ease'
url: /2012/07/08/sar-sysstat-linux-performance-statistics-with-ease

---

Whenever I perform any type of activity that requires me to look at historical system statistics such as load average, CPU utilization, I/O wait state, or even memory usage; I usually skip the System Monitoring Applications like Nagios or Zenoss and start running the `sar` command. While I'm not saying that sar completely replaces those tools, I am saying that sar is quick and dirty and if all you want is some raw numbers from a certain time frame; sar is a great tool.

## What is sar?

sar (System Activity Reporter) is a command that ships with the `sysstat` package. Sysstat is a collection of Unix tools used for performance monitoring, the package includes tools such as `iostat`, `mpstat`, `pidstat`, `sadf` and `sar`.

Along with the real time commands sysstat will install a cronjob that will run every 10 minutes and collect the systems performance information. Sar is the command you can use to read the collected information.

## Setting up sysstat

Below you will find instructions on how to install, configure, and use sysstat & sar. I personally run sysstat collection on all of the servers under my care as the benefits of having this data far out weighs any reason you could think of not installing it (I can't think of any).

### Install and Configure

Installing sysstat is pretty simple and is in the repositories for most Linux Distributions.

#### Installing with apt:
     
     $ sudo apt-get install sysstat

#### Installing with yum:
     
     $ sudo yum install sysstat

### Enable sysstat collection

In order to enable sysstat collection we will need to edit the `/etc/default/sysstat` file.

**Edit the config file:**
     
     # vi /etc/default/sysstat

**Find:**
     
     # Should sadc collect system activity informations? Valid values
     # are "true" and "false". Please do not put other values, they
     # will be overwritten by debconf!
     ENABLED="false"

**Modify to:**
     
     # Should sadc collect system activity informations? Valid values
     # are "true" and "false". Please do not put other values, they
     # will be overwritten by debconf!
     ENABLED="true"

Once you have made the change save and exit the file; from here every time the cronjob is run sysstat will collect system information.

#### Changing the collection interval (optional)

By default sysstat will collect data every 10 minutes, some people (like me) will want a shorter collection interval. In order to accomplish this you can simply modify the cronjob that runs every 10 minutes.

**Edit the cronjob file:**
     
     # vi /etc/cron.d/sysstat

**Find:**
     
     # Activity reports every 10 minutes everyday
     5-55/10 * * * * root command -v debian-sa1 > /dev/null && debian-sa1 1 1

**Modify to:**
     
     # Activity reports every 5 minutes everyday
     */5 * * * * root command -v debian-sa1 > /dev/null && debian-sa1 1 1

Now you can save and exit the file and simply wait 5 minutes for the next run of sysstat to verify that you are collecting data.

#### Keep sysstat log files longer than 1 week (optional)

By default sysstat will only retain its log files (historical performance statistics) for 7 days, personally I prefer to keep these files around for at least 31 days. To keep these files longer simply edit the `/etc/sysstat/sysstat`  config file.

**Edit the config file:**
     
     # vi /etc/sysstat/sysstat

**Find:**

     # How long to keep log files (in days).
     # Used by sa2(8) script
     # If value is greater than 28, then log files are kept in
     # multiple directories, one for each month.
     HISTORY=7

**Modify to:**
     
     # How long to keep log files (in days).
     # Used by sa2(8) script
     # If value is greater than 28, then log files are kept in
     # multiple directories, one for each month.
     HISTORY=31

Save and exit the file and you will now be keeping 31 days of log files.

### Accessing the Performance Statistics with sar

There are a metric ton of methods of getting data out of sar, below are a few options that I use commonly.

#### Access Previous Days Data

Before I start giving you examples of ways to extract performance statistic goodness via sar I first want to cover the default output of sar. By default sar will output the current days statistics depending on what options you give it; in order to get a previous days data from sar you must find that days log file and specify it with `-f /path/to/file`.

**Example:**
     
     # sar -f /var/log/sysstat/sa04

The log files for sar are contained within the `/var/log/sysstat` or `/var/log/sa` directory depending on your distributions implementation. The sa log files have a bit of an interesting naming scheme which isn't used very often in Unix or Linux. The files end with a number that denotes the day example sa04 is actually the file from the 4th day of the current month.

This ls listing may help explain it easier.
     
     # ls -la sa[0-9]*
     -rw-r--r-- 1 root root 254604 2012-07-02 00:00 sa01 << This file is for 2012-07-01
     -rw-r--r-- 1 root root 254604 2012-07-03 00:00 sa02
     -rw-r--r-- 1 root root 254604 2012-07-04 00:00 sa03
     -rw-r--r-- 1 root root 254604 2012-07-05 00:00 sa04
     -rw-r--r-- 1 root root 254604 2012-07-06 00:00 sa05
     -rw-r--r-- 1 root root 254604 2012-07-07 00:00 sa06
     -rw-r--r-- 1 root root 220044 2012-07-07 20:55 sa07 << This file is for 2012-07-07 (The current day)
     -rw-r--r-- 1 root root 254604 2012-06-30 00:00 sa29 << This file is for 2012-06-29
     -rw-r--r-- 1 root root 254604 2012-07-01 00:00 sa30 << This file is for 2012-06-30

Note: Per the config files comments if you are keeping the log files longer than 28 days the files will be contained in a sub directory to denote the month

The `-f` flag can be used with all of the examples below to show data from a specific day.

#### CPU Information

The following command prints out the collective CPU performance information
     
     # sar
     Linux 3.2.0-26-generic (workstation) 07/07/2012 _x86_64_ (1 CPU)
     01:35:02 PM CPU %user %nice %system %iowait %steal %idle
     01:40:01 PM all 1.30 0.00 0.66 0.31 0.00 97.73
     01:45:02 PM all 1.12 0.00 0.43 0.22 0.00 98.23

If you want to display the CPU information broken down rather than summarized you can use the `-P` flag.
     
     # sar -P ALL
     Linux 3.2.0-26-generic (workstation) 07/07/2012 _x86_64_ (1 CPU)
     01:35:02 PM CPU %user %nice %system %iowait %steal %idle
     01:40:01 PM all 1.30 0.00 0.66 0.31 0.00 97.73
     01:40:01 PM 0 1.30 0.00 0.66 0.31 0.00 97.73
     01:40:01 PM CPU %user %nice %system %iowait %steal %idle
     01:45:02 PM all 1.12 0.00 0.43 0.22 0.00 98.23
     01:45:02 PM 0 1.12 0.00 0.43 0.22 0.00 98.23

I only have 1 CPU on my test virtual machine but if you have a multiprocessor machine the output will have more CPU's.

#### I/O Statistics

The `-b` flag will show the summarized I/O Statistics.
     
     # sar -b
     Linux 3.2.0-26-generic (workstation) 07/07/2012 _x86_64_ (1 CPU)
     01:35:02 PM tps rtps wtps bread/s bwrtn/s
     01:40:01 PM 0.88 0.04 0.84 1.50 8.67
     01:45:02 PM 0.68 0.00 0.68 0.00 6.94
     01:50:02 PM 0.67 0.00 0.67 0.00 6.83
     01:55:01 PM 1.58 0.62 0.96 19.72 10.29

#### Disk Utilization

The `-d` flag will show the activity of your block devices, this output is similar to iostat's.
     
     # sar -d
     Linux 3.2.0-26-generic (workstation) 07/07/2012 _x86_64_ (1 CPU)
     01:35:02 PM DEV tps rd_sec/s wr_sec/s avgrq-sz avgqu-sz await svctm %util
     01:40:01 PM dev8-0 0.32 0.75 4.34 16.00 0.03 92.34 21.64 0.69
     01:40:01 PM dev252-0 0.56 0.75 4.34 9.05 0.05 86.69 12.26 0.69
     01:40:01 PM dev252-1 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00
     01:45:02 PM dev8-0 0.24 0.00 3.47 14.25 0.03 113.81 26.41 0.64
     01:45:02 PM dev252-0 0.43 0.00 3.47 8.00 0.04 98.55 14.86 0.64
     01:45:02 PM dev252-1 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00

#### Paging Information

The -B flag will show the systems paging information, this is useful for determining if your system is paging frequently.
     
     # sar -B
     Linux 3.2.0-26-generic (workstation) 07/07/2012 _x86_64_ (1 CPU)
     01:35:02 PM pgpgin/s pgpgout/s fault/s majflt/s pgfree/s pgscank/s pgscand/s pgsteal/s %vmeff
     01:40:01 PM 0.37 2.17 56.25 0.01 21.46 0.00 0.00 0.00 0.00
     01:45:02 PM 0.00 1.73 34.75 0.00 14.49 0.00 0.00 0.00 0.00
     01:50:02 PM 0.00 1.71 43.66 0.00 17.17 0.00 0.00 0.00 0.00

#### Memory Usage

This is very useful for figuring out what your memory utilization was historically.

Note: Before freaking out that your memory is nearly completely utilized please visit [Linux Ate My RAM](http://www.linuxatemyram.com/)
     
     # sar -r
     Linux 3.2.0-26-generic (workstation) 07/07/2012 _x86_64_ (1 CPU)
     01:35:02 PM kbmemfree kbmemused %memused kbbuffers kbcached kbcommit %commit kbactive kbinact
     01:40:01 PM 39912 205528 83.74 53080 98860 65720 10.03 73036 99284
     01:45:02 PM 39912 205528 83.74 53080 98868 65724 10.03 73112 99192
     01:50:02 PM 39852 205588 83.76 53084 98868 65720 10.03 73124 99196

#### Swap Usage

This option goes hand in hand with the memory usage option, you can use this option to figure out when your system started swapping.
     
     # sar -S
     Linux 3.2.0-26-generic (workstation) 07/07/2012 _x86_64_ (1 CPU)
     01:35:02 PM kbswpfree kbswpused %swpused kbswpcad %swpcad
     01:40:01 PM 409180 416 0.10 196 47.12
     01:45:02 PM 409180 416 0.10 196 47.12
     01:50:02 PM 409180 416 0.10 196 47.12

#### Huge Pages Usage

The -H option will give you the historical huge pages usage, this is especially helpful for Oracle database servers.
     
     # sar -H
     Linux 3.2.0-26-generic (workstation) 07/07/2012 _x86_64_ (1 CPU)
     01:35:02 PM kbhugfree kbhugused %hugused
     01:40:01 PM 0 0 0.00
     01:45:02 PM 0 0 0.00

#### Network Device Statistics

The -n option can show you network statistics, there are quite a few options for this but the device statistics has been the most useful for me.
     
     # sar -n DEV
     Linux 3.2.0-26-generic (workstation) 07/07/2012 _x86_64_ (1 CPU)
     01:35:02 PM IFACE rxpck/s txpck/s rxkB/s txkB/s rxcmp/s txcmp/s rxmcst/s
     01:40:01 PM lo 0.00 0.00 0.00 0.00 0.00 0.00 0.00
     01:40:01 PM eth0 0.54 0.39 0.04 0.05 0.00 0.00 0.00
     01:45:02 PM lo 0.00 0.00 0.00 0.00 0.00 0.00 0.00
     01:45:02 PM eth0 0.07 0.05 0.00 0.01 0.00 0.00 0.00
     01:50:02 PM lo 0.00 0.00 0.00 0.00 0.00 0.00 0.00

#### If all else fails get everything

The sar man page has even more examples of usage than the above, if you have not found what your looking for here than you can try the man page for specifics. If you are in too much of a hurry to figure it all out you can use `sar -A` to output all of the sysstat collected data for that day; you may want to output that to a file as it is quite a bit of data.
     
     # sar -A
     <too much to list here>

---
authors:
- Benjamin Cane
categories:
- Administration
- Linux
- Linux Distributions
- Red Hat
- Troubleshooting
- Ubuntu
date: '2011-11-02T20:00:06'
description: This article shows a simple method to validate whether or not a cronjob
  ran on both Red Hat/Fedora based and Debian based Linux Systems
draft: false
header:
  caption: ''
  image: ''
tags:
- config
- cron
- crond
- cronjob
- crons
- daemon
- debian
- fedora
- linux
- linux scheduled jobs
- linux scheduled tasks
- log message
- logs
- scheduled tasks
- tech
- ubuntu
- unix
- unix linux
title: How to check if a cron job ran
url: /2011/11/02/did-my-cronjob-run

---

Cron is a time based scheduled task daemon that runs on most common Unix/Linux distributions. Because cronjobs are time based sometimes it is necessary to validate that the job ran at the scheduled time. Sometimes people will configure a cron to send the output of the script to a user via system mail or redirect the output to a file; however not all crons are setup the same and many times they may be configured to send output to /dev/null hindering any ability to validate the job ran.

Today I will show how to validate that cron at least attempted to run the command even if the output is nowhere to be found.

## **Finding the appropriate log file**

crond unless configured otherwise will send a log message to syslog every time it invokes a scheduled job. The simplest way to validate that cron tried to run the job is to simply check the appropriate log file; the log files however can be different from system to system.

In order to determine which log file contains the cron logs we can simply check the occurrence of the word cron in the log files within `/var/log`.

**Fedora:**
     
     # grep -ic cron /var/log/* | grep -v :0
      ./cron:52
      ./dracut.log:2
      ./messages:1
      ./secure:6

**Ubuntu/Debian:**

     # grep -ic cron /var/log/* | grep -v :0
      ./auth.log:1246
      ./auth.log.1:3054
      ./bootstrap.log:3
      ./syslog:187
      ./syslog.1:220

On the examples above the cron log file of Fedora is an obvious place to look not only because of the name but because it is the only log file with a significant amount of lines that contain the word cron. On Ubuntu and Debian it is not so obvious; the auth.log files contain the most lines from cron but these do not actually contain the lines we want.

## Check the syslog configuration

Another method of finding which log file to check is to simply check the syslog configuration as the syslog configuration will show either a specific line for cron or cron being defaulted to a general log file. The syslog config file may be `/etc/rsyslog.conf` or `/etc/syslog.conf` depending on what syslog service you have installed.
     
     # grep cron /etc/rsyslog.conf
      *.info;mail.none;authpriv.none;cron.none    /var/log/messages
      # Log cron stuff
      cron.*                      /var/log/cron

## Checking the log file

Once you have figured out which log file has the information you can simply search through the log file for the last run or a specific run of your cronjob.

**Example of a good run:**

     # grep -i debian-sa1 syslog | tail -1
     Nov 02 15:05:01 testbox CRON[32106]: (root) CMD (command -v debian-sa1 > /dev/null && debian-sa1 1 1)

The above example shows the log message of a cronjob that was at least run by crond; however not all messages may be successful. If a job was unable to be run due to an error the log entry may appear as so.

**Example of a failed run:**

     Nov 02 17:10:01 testbox CRON[2210]: (testuser) WRONG INODE INFO (crontabs/testuser)

The above message was shown because the crontab file has permissions of 666 which is an insecure and invalid permission for crond.

## Checking if cron is configured to log

If you have run through the above and were not able to find any log files with cron information inside than it is possible that crond is configured to not log at all. To validate whether cron is configured to send messages to syslog you can simply check /etc/default/cron.

**/etc/default/cron:**

     # Extra options for cron, see cron(8)
     # For example, set a higher log level to audit cron's work
     # EXTRA_OPTS="-L 0"

If cron is started with `-L 0` as an extra option than this disables logging by cron, you can modify the 0 to either 1 or 2 depending on how verbose you want cron to be and restart crond.

**/etc/default/cron:**
     
     # Extra options for cron, see cron(8)
     # For example, set a higher log level to audit cron's work
     # EXTRA_OPTS="-L 2"

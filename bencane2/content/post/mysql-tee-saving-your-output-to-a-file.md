---
authors:
- Benjamin Cane
categories:
- Applications
- Command Line
- Databases
- MySQL
date: '2011-12-26T16:00:21'
description: Learn to use the MySQL tee command to save the MySQL CLI output to a
  file and to your tty
draft: false
header:
  caption: ''
  image: ''
tags:
- linkedin
- linux
- mysql
- mysql cli
- tech
- tee
- unix
title: 'MySQL: tee saving your output to a file'
url: /2011/12/26/mysql-tee-saving-your-output-to-a-file

---

Tee is a unix command that takes the standard out output of a Unix command and writes it to both your terminal and a file. Until recently I never knew there was a MySQL client command that performed the same function. Today I will show you an example of how to use it.

First login to the MySQL CLI (command line interface)
     
     $ mysql -uroot -p
     Enter password:
     Welcome to the MySQL monitor.  Commands end with ; or g.
     Your MySQL connection id is 24839

Once you are in you will have a command prompt. From there simply type tee and the file path and name you want to save to.
     
     mysql> tee /var/tmp/mysql_tee.out
     Logging to file '/var/tmp/mysql_tee.out'
     mysql> use mysql;
     Reading table information for completion of table and column names
     You can turn off this feature to get a quicker startup with -A
     
     Database changed
     mysql> show tables;
     +---------------------------+
     | Tables_in_mysql           |
     +---------------------------+
     | columns_priv              |
     | db                        |
     | event                     |
     | func                      |
     | general_log               |
     | help_category             |
     | help_keyword              |
     | help_relation             |
     | help_topic                |
     | host                      |
     | ndb_binlog_index          |
     | plugin                    |
     | proc                      |
     | procs_priv                |
     | servers                   |
     | slow_log                  |
     | tables_priv               |
     | time_zone                 |
     | time_zone_leap_second     |
     | time_zone_name            |
     | time_zone_transition      |
     | time_zone_transition_type |
     | user                      |
     +---------------------------+
     23 rows in set (0.00 sec)

Now just check your file and make sure your commands were logged.

     $ ls -la /var/tmp/mysql_tee.out
     -rw-r--r-- 1 ubuntu ubuntu 1030 2011-12-22 01:43 /var/tmp/mysql_tee.out

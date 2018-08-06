---
authors:
- Benjamin Cane
categories:
- All Articles
- Applications
- Databases
- How To and Tutorials
- Linux
- MySQL
- Ubuntu
date: '2012-12-05T22:35:34'
description: How to install MySQL on Ubuntu or Debian based Linux Systems using apt-get
draft: false
header:
  caption: ''
  image: ''
tags:
- apt
- apt-get
- debian
- linux
- linux os
- mysql
- mysql connection
- rdbms
- relational database management
- relational database management system
- ubuntu
- ubuntu os
title: Installing MySQL on Ubuntu/Debian
url: /2012/12/05/installing-mysql-on-ubuntudebian

---

MySQL is the most popular open source relational database management system (RDBMS) in the world. MySQL is used by everyone from the simple small business website to the large internet giants like Facebook, Google or Amazon. In fact the contents of this page are even stored within MySQL.

Installing MySQL is a fairly common task for any systems administrator; especially if that administrator is running a standard LAMP stack (Linux, Apache, MySQL & PHP/Python/Perl).

The following steps outline how to install mysql on a Debian/Ubuntu server. These steps are fairly similar for Red Hat based distributions and can be used by simply replacing apt-get with yum.

## Check whether MySQL is installed
     
     root@server:/nfs# dpkg --list mysql
      No packages found matching mysql.

Depending on your system you may see packages with mysql in the name, if you do not see mysql-server than it is not likely that you have mysql installed.

## Installing MySQL with apt-get
     
     root@server:/nfs# apt-get install mysql-server mysql-client

During the installation you will be asked to provide a root password. I suggest making this password different than your servers root password especially if you have DBA's managing the MySQL instance but do not want them to have access to root on the server.

The `apt-get` command will also install the mysql-client package which is necessary to login to mysql from the server itself.

## Verifying MySQL is installed

MySQL will start automatically after the installation, to validate that it is installed and running properly you can do the following steps

### Verify MySQL is listening
     
     root@server:/nfs# netstat -na | grep 3306
      tcp 0 0 127.0.0.1:3306 0.0.0.0:* LISTEN

### Connect via the client
     
     root@server:~# mysql -u root -p
      Enter password:
      Welcome to the MySQL monitor. Commands end with ; or g.
      Your MySQL connection id is 38
      Server version: 5.5.28-0ubuntu0.12.04.2 (Ubuntu)

     Copyright (c) 2000, 2012, Oracle and/or its affiliates. All rights reserved.
     
     Oracle is a registered trademark of Oracle Corporation and/or its
      affiliates. Other names may be trademarks of their respective
      owners.
     
     Type 'help;' or 'h' for help. Type 'c' to clear the current input statement.

     mysql>

If the above commands work than you are able to connect to mysql on localhost and start using it.

## Change the listening address for MySQL

By default MySQL will listen on localhost (127.0.0.1) only, if you want to connect to MySQL from another server you will need to change this IP address to whatever IP you want to connect to. To do this simply edit the `my.cnf` file and change the bind-address attribute
     
     root@server:/nfs# vi /etc/mysql/my.cnf

**Find:**
     
     # Instead of skip-networking the default is now to listen only on
      # localhost which is more compatible and is not less secure.
      bind-address = 127.0.0.1

**Replace with:**
     
     # Instead of skip-networking the default is now to listen only on
      # localhost which is more compatible and is not less secure.
      bind-address = your.ip.address.here

Once the IP has been changed simply restart mysql.
     
     root@server:~# restart mysql

or
     
     root@server:~# service mysql restart

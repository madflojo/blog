---
authors:
- Benjamin Cane
categories:
- All Articles
- Applications
- How To and Tutorials
- Sysadmin Tools
date: '2013-10-14T07:20:46'
description: RackTables is an interesting IT inventory tracking system that can be
  used to track IP addresses as well as the hardware they are attached to.
draft: false
header:
  caption: ''
  image: ''
tags:
- apache
- ip inventory
- lamp
- linux
- php
- racktables
- ubuntu
title: Install RackTables and start tracking your IP address inventory
url: /2013/10/14/install-racktables-and-start-tracking-your-ip-address-inventory

---

Recently while I was scouring through a spreadsheet of "unallocated" IP addresses, I thought to myself. There has to be a better way to manage an inventory of IP addresses, and while I'm at it maybe even provide a list of provisioned servers.

After some googling I found myself on [RackTables.org](http://RackTables.org) the home of an **open source project** that aims to provide just what I was looking for. An Inventory system that tracks and manages Servers, Racks, IP Addresses and just about everything else in a data center.

For today's article I will cover the steps necessary to get RackTables up and running and ready for you to start tracking your data center inventory.

## Taking care of the prerequisites

In order to run RackTables we will need to setup a basic webserver with PHP and a MySQL database. Since RackTables is written in PHP in theory it can be run on any webserver that runs PHP. To keep things simple for this article however, I am going to walk through setting up a very basic LAMP stack using Ubuntu Server 12.04.

### Installing Apache with PHP Support

To install Apache and PHP we will be using the `apt` package manager. If you are installing this on Red Hat or CentOS systems than the packages will be similar however you may need to modify the naming convention to match the packages within `yum`.

    # apt-get install apache2 apache2.2-common libapache2-mod-php5 \
     php5-snmp php5-ldap php5 php5-common php5-gd curl php5-mysql \
     mysql-client mysql-common

Apt may suggest additional packages to install, I suggest installing them as they may come in handy at a later time.

### Installing MySQL Server

You may have noticed that I only installed the **php5-mysql** and **mysql-client** packages on the system. I am splitting the MySQL server package install as a second step as you may want to install the **mysql-server** package on a different server. Allowing you to separating the database and the RackTables application.

    #apt-get install mysql-client mysql-common mysql-server

During the **mysql-server** installation you will be prompted to enter a MySQL root user password. This password does not need to be the same as the systems root users password. Make sure you remember this password as you will need it in upcoming steps.

## Installing RackTables

Now that we have a basic LAMP setup we can get started with installing the RackTables.

### Creating a System User for RackTables

To make things a bit more secure we are going to have all of the RackTables php files owned as a unprivileged user. This is a more secure than having the php files owned as root or the apache/nobody user.

    # useradd -u 4000 -g users -s /sbin/nologin -c "RackTables User" -md /home/racktables racktables

Feel free to put the **racktables** user into a different users group or change the UID. If you aren't sure exactly what these do than I would suggest checking out my article on [adding users in Linux](http://bencane.com/2013/06/24/adding-and-modifying-users-groups-in-linux/).

### Creating the RackTables Database

Before deploying the php files we will want to create a database on the MySQL server. To create the database we will need to login to the MySQL server via the MySQL Client package we installed. Hopefully you remember the MySQL root users password, as we will need it during this step.

    # mysql -u root -p 
    Enter password:

Now that we are logged into the MySQL server we can create the database

    mysql> create database racktables;
    Query OK, 1 row affected (0.01 sec)

### Creating the RackTables Database User

In theory we could let the racktables application login to MySQL via the root MySQL user, but that wouldn't be very secure. The below commands will create a database user named rackuser that only has access to the racktables database.

    mysql> grant all privileges on racktables.* TO
     -> 'rackuser'@'localhost' identified by 'SecretPass';

MySQL keeps a cache of user privileges, whenever you make a change it is advisable to flush the cache to avoid confusion.

    mysql> flush privileges;
    Query OK, 0 rows affected (0.00 sec)

At this point we are done with the MySQL CLI and we can logout with the exit command.

    mysql> exit
    Bye

It is a good idea to test that the user/password worked before continuing. We will do this by logging into the MySQL Server via the CLI the same way we did when we created the database.

    # mysql -u rackuser -pSecretPass
    Welcome to the MySQL monitor. Commands end with ; or \g.

### Download and Deploy the Application

RackTables is an open source project and is downloadable from SourceForge. Below we will download and deploy the application files.

**As the root user:**

    # cd /var/tmp
    # su -s /bin/bash racktables

**As the racktables user:**

    $ wget http://sourceforge.net/projects/racktables/files/RackTables-0.20.5.tar.gz
    $ tar -xvzf RackTables-0.20.5.tar.gz

**As the root user:**

    # mv RackTables-0.20.5/wwwroot /var/www/racktables

### Go to the installation page

Apache has a default html documents directory of `/var/www` by putting the RackTables files into `/var/www/racktables` this will allow us to go to the application by typing **http://server_ip/racktables**.

The initial page should provide you with a link to continue the 6 steps of installation.

### Follow the 6 Installation Steps

#### Step 1: Click proceed to start the installation process

The first step is self explanatory, simply click proceed.

#### Step 2: Check for missing packages

The second step will display if any of the php modules are missing. If any are missing you can install them using `apt-get`, for example when I was writing this article I missed the GD module.

**Example:**

    # apt-get install php5-gd

#### Step 3: Create the secret file

RackTables stores the database information in the secret file. We will set the permissions to 666 allowing Apache to write the information into this file during install. It is important to remember to reset the permissions to 644 at the end of the installation.

    # touch /var/www/racktables/inc/secret.php
    # chmod 666 /var/www/racktables/inc/secret.php

#### Step 4: Insert the Database Information

Step 4 will import the database tables and structure as well as place the database information into the secret file. On this step simply input the database information into the form and click proceed.

    Server: localhost
    Port: 3306
    Database Name: racktables
    Username: rackuser
    Password: Your Password

If you have been following this article to the letter the information above should work, if not you will need to put in the correct information.

#### Step 5: Set the Administrator Password

After the database is imported you will be prompted for an administrator password. Simply set this and proceed.

#### Step 6: Accept the Installation and Proceed

The last step should be a success message stating that RackTables has been installed properly. At this point we will need to reset the secret file's permissions.

    # chmod 644 /var/www/racktables/inc/secret.php

Now that the installation is finished you can start creating objects (servers, network devices, what not), adding your IP subnets and stop wondering when the last time this old spreadsheet has been updated.

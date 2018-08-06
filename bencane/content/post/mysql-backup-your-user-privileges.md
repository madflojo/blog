---
authors:
- Benjamin Cane
categories:
- Administration
- All Articles
- Applications
- Databases
- How To and Tutorials
- MySQL
date: '2011-09-15T20:01:06'
description: How to backup your mysql privileges to a CSV file
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- mysql
- tech
title: 'mysql: Backup your user privileges'
url: /2011/09/15/mysql-backup-your-user-privileges

---

While I am sure there are multiple ways to do this and some probably easier here is a way to backup your mysql user privileges to a CSV file.

First you will need to get to the mysql cli.

    # mysql -uroot -p  
    Enter password:
    Welcome to the MySQL monitor. Commands end with ; or g.  
    Your MySQL connection id is 35083  
    Server version: 5.0.51a-24+lenny3 (Debian)
    Type 'help;' or 'h' for help. Type 'c' to clear the buffer.

After you are logged in you will need to select which database to use. In this case its the db named mysql.

    mysql> use mysql;
    Reading table information for completion of table and column names

Now you are going to need to backup the db table. We do not care about the test database so this statement is excluding it.

    mysql> select * from db where db not like "test%" INTO outfile "/var/tmp/mysql.db.dump" FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY 'n';  
    Query OK, 5 rows affected (0.11 sec)

And finally the user table. In this case I don't care about the root user or anything that matches Debian. So we will exclude these as well.

    mysql> select * from user where user != "root" && user not like "debian%" INTO outfile "/var/tmp/mysql.users.dump" FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY 'n';  
    Query OK, 5 rows affected (0.00 sec)

Now we can see our CSV files.

    # ls -la /var/tmp/mysql.*  
    -rw-rw-rw- 1 mysql mysql 531 2011-09-14 20:49 /var/tmp/mysql.db.dump  
    -rw-rw-rw- 1 mysql mysql 990 2011-09-14 20:49 /var/tmp/mysql.users.dump

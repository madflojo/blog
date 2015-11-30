
Mysqldump is a great utility for backing up or exporting a database to a flat file. This flat file can then be used to import the database or databases into another mysql database or even another database server like postgre depending on the options you use.

To perform a very simple backup of the mysql database you can simply just setup a cronjob that runs mysqldump at whatever interval you want.

## Example: Backup all databases

     # /usr/bin/mysqldump -uBACKUPUSER -pPASSWORD --all-databases > /path/to/flatfile.sql

The above example backs up all of the databases on the system (even the mysql internal database); if you have a specific database you want to backup you can simply specify it on the command line.

## Example: Backup a specific database

     # /usr/bin/mysqldump -uBACKUPUSER -pPASSWORD DATABASE > /path/to/flatfile.sql

In regards to the user that you are using to backup the database you have two options. You can use a user that has read/write privileges on all of the databases (Less Secure) or setup a new user with read only access on all of the databases (More Secure).

## Example: Creating a read only mysql user
     
     # /usr/bin/mysql -uroot -p
     Enter password:
     Welcome to the MySQL monitor.  Commands end with ; or g.
     Your MySQL connection id is 253404
     Server version: 5.1.54-1ubuntu4 (Ubuntu)
     
     Copyright (c) 2000, 2010, Oracle and/or its affiliates. All rights reserved.
     This software comes with ABSOLUTELY NO WARRANTY. This is free software,
     and you are welcome to modify and redistribute it under the GPL v2 license
     
     Type 'help;' or 'h' for help. Type 'c' to clear the current input statement.
     
     mysql> GRANT LOCK TABLES, SELECT ON *.* TO 'BACKUPUSER'@'%' IDENTIFIED BY 'PASSWORD';
     Query OK, 0 rows affected (0.01 sec)
     
     mysql> flush privileges;
     Query OK, 0 rows affected (0.00 sec)
     
     mysql> Bye

If you only want the user to have permissions on a specific database you can just modify the command above to match the following.
     
     GRANT LOCK TABLES, SELECT ON DATABASE.* TO 'BACKUPUSER'@'%' IDENTIFIED BY 'PASSWORD';

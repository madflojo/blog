---
authors:
- Benjamin Cane
categories:
- All Articles
- Applications
- Databases
- How To and Tutorials
- MySQL
date: '2011-10-19T07:11:25'
description: How to setup a basic mysql database and database user with privileges
  to only the newly created database
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- mysql
- tech
- unix
title: 'mysql: Creating a db and user'
url: /2011/10/19/mysql-creating-a-db-and-user

---

While the specific commands below were used to create a test database for wordpress the same commands will apply for most situations where you want to create a mysql database and a user with appropriate privileges to that database.

    $ mysql -uroot -p  
    Enter password:
    Welcome to the MySQL monitor. Commands end with ; or g.  
    Your MySQL connection id is 39304  
    Server version: 5.1.54-1ubuntu4 (Ubuntu)

First log into the mysql command line interface using the mysql command. The -u is specifying to use the root user and -p tells mysql to ask for the password. If you don't specify -p you will receive the error below.

    $ mysql -uroot  
    ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: NO)

Once you are logged in you will create the test_wp database.

    mysql> create database test_wp;  
    Query OK, 1 row affected (0.02 sec)

After the database is created you will need to create the user and give it privileges using the grant command.

**Warning:** The grant command can give this user privileges to not only your newly created database but all databases if used improperly. Make sure that you specify the database as per the command below.

    mysql> grant all privileges on test_wp.* TO '<username>' identified by "<password>";  
    Query OK, 0 rows affected (0.07 sec)

Once you've created the user you have to flush the privileges information that mysql caches; if you don't do this mysql may not recognize the changes.

    mysql> flush privileges;  
    Query OK, 0 rows affected (0.04 sec)

Now you can use the commands below to verify everything was created properly.

    mysql> show databases;  
    +----------------------+  
    | Database       |  
    +----------------------+  
    | test_wp     |  
    | mysql        |  
    +----------------------+  
    8 rows in set (0.00 sec)  
    mysql> select * from mysql.user where user = "<username>"G  
    *************************** 1. row ***************************  
            Host: %  
            User: <truncated>  
          Password: <truncated>  
         Select_priv: N  
         Insert_priv: N  
         Update_priv: N  
         Delete_priv: N  
         Create_priv: N  
          Drop_priv: N  
         Reload_priv: N  
        Shutdown_priv: N  
        Process_priv: N  
          File_priv: N  
         Grant_priv: N  
       References_priv: N  
         Index_priv: N  
         Alter_priv: N  
        Show_db_priv: N  
         Super_priv: N  
    Create_tmp_table_priv: N  
      Lock_tables_priv: N  
        Execute_priv: N  
       Repl_slave_priv: N  
      Repl_client_priv: N  
      Create_view_priv: N  
       Show_view_priv: N  
     Create_routine_priv: N  
     Alter_routine_priv: N  
      Create_user_priv: N  
          ssl_type:  
         ssl_cipher:  
         x509_issuer:  
        x509_subject:  
        max_questions: 0  
         max_updates: 0  
       max_connections: 0  
    max_user_connections: 0  
    1 row in set (0.00 sec)




    mysql> select * from mysql.db where user = '<username>'G  
    *************************** 1. row ***************************  
            Host: %  
             Db: test_wp  
            User: <username>  
         Select_priv: Y  
         Insert_priv: Y  
         Update_priv: Y  
         Delete_priv: Y  
         Create_priv: Y  
          Drop_priv: Y  
         Grant_priv: N  
       References_priv: Y  
         Index_priv: Y  
         Alter_priv: Y  
    Create_tmp_table_priv: Y  
      Lock_tables_priv: Y  
      Create_view_priv: Y  
       Show_view_priv: Y  
     Create_routine_priv: Y  
     Alter_routine_priv: Y  
        Execute_priv: Y  
    1 row in set (0.00 sec)

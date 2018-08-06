---
authors:
- Benjamin Cane
categories:
- Administration
- How To and Tutorials
- Linux Commands
- Rdiff-Backup
date: '2013-05-20T16:10:30'
description: A guide on setting up rdiff-backup and using sudo to run rdiff-backup
  without running it as the root user
draft: false
header:
  caption: ''
  image: ''
tags:
- backup package
- backup server
- backup tool
- linux
- linux os
- rdiff-backup
- red hat
- red hat os
- sudo
- ubuntu linux
- ubuntu os
title: Securely backing up your files with rdiff-backup and sudo
url: /2013/05/20/securely-backing-up-your-files-with-rdiff-backup-and-sudo

---

Backups are important, whether you are backing up your databases or your wedding pictures. The loss of data can ruin your day. While there is a huge [list of backup software](http://en.wikipedia.org/wiki/List_of_backup_software) to choose from; some good, some not so good. One of the tools that I have used for years is rdiff-backup.

rdiff-backup is a rsync delta based backup tool that both stores a full mirror and incremental changes. It determines changes based on the rsync method of creating small delta files, which allows for rdiff-backup to restore files to any point in time (within the specified retention period).

In the examples below I will refer to two servers names, **backup-server** and **server**. The names are pretty self-explanatory but just in case, **backup-server** is the location where I permanently store files copied (backed up) from **server**.

## Setting up rdiff-backup

Installing rdiff-backup is easy considering most Linux distributions include it into their default repositories. In this article I will be using Ubuntu for my example systems.

**Note:** For Red Hat you will need to enable the EPEL repository to install rdiff-backup via YUM.

#### Installing

In order for rdiff-backup to work both the source and destination will require the rdiff-backup package. You can install it via `apt-get`.

**On backup-server**:

    root@backup-server# apt-get install rdiff-backup

**On server**:

    root@server# apt-get install rdiff-backup

#### Validate rdiff-backup versions match

One of the quirky things about rdiff-backup is that the tool does not support backwards capability with older versions. For this reason it is best to make sure that your rdiff-backup versions are the same on both servers.

**On backup-server:**

    root@backup-server# rdiff-backup --version
    rdiff-backup 1.2.8

**On server:**

    root@server# rdiff-backup --version
    rdiff-backup 1.2.8

#### Setting up SSH Keys

By default rdiff-backup uses SSH to communicate with remote systems to avoid typing a password every time rdiff-backup runs we will need to set-up SSH keys with passphrase-less authentication.

**On backup-server:**

    root@backup-server# ssh-keygen -t rsa
    Generating public/private rsa key pair.
    Enter file in which to save the key (/root/.ssh/id_rsa):
    Created directory '/root/.ssh'.
    Enter passphrase (empty for no passphrase):
    Enter same passphrase again:
    Your identification has been saved in /root/.ssh/id_rsa.
    Your public key has been saved in /root/.ssh/id_rsa.pub.

When asked leave the passphrase empty.

Once you have the SSH key generated you will need to copy the contents of `/root/.ssh/id_rsa.pub` to the remote servers for key-based authentication. For our configuration we will use a non-privileged user account (test), as this will let us implement rdiff-backup without giving the backup-server full access to the systems being backed up.

**On backup-server:**

    root@backup-server:# scp /root/.ssh/id_rsa.pub test@server:/var/tmp/id_rsa.pub.temp

**On server:**

    test@server:$ cat /var/tmp/id_rsa.pub.temp >> ~/.ssh/authorized_keys

You should now be able to SSH from **backup-server** to **server** without being asked for a password.

## Running backup jobs

Now that **backup-server** is able to SSH to **server** without being asked a password and rdiff-backup is the same version on both systems we are able to perform the first backup.

The directory we will backup today is `/var/tmp/backmeup` and we will be backing it up to `/var/tmp/backups/server.example.com/`. I personally prefer to backup to a directory named after the originating server, that way there is no question as to where the files came from.

**On backup-server:**

    root@backup-server:# mkdir -p /var/tmp/backups/server.example.com
    root@backup-server:# rdiff-backup test@server.example.com::/var/tmp/backmeup /var/tmp/backups/server.example.com/

rdiff-backup has now created a mirror of the `/var/tmp/backmeup` directory from **server.example.com** in `/var/tmp/backups/server.example.com`.

    root@backup-server:# ls -la /var/tmp/backups/server.example.com/
    total 52
    drwxr-xr-x 3 root root 4096 May 19 13:07 .
    drwxr-xr-x 3 root root 4096 May 19 13:53 ..
    -rw-r--r-- 1 root root 25 May 19 13:07 10.file
    -rw-r--r-- 1 root root 24 May 19 13:07 1.file
    -rw-r--r-- 1 root root 24 May 19 13:07 2.file
    -rw-r--r-- 1 root root 24 May 19 13:07 3.file
    -rw-r--r-- 1 root root 24 May 19 13:07 4.file
    -rw-r--r-- 1 root root 24 May 19 13:07 5.file
    -rw-r--r-- 1 root root 24 May 19 13:07 6.file
    -rw-r--r-- 1 root root 24 May 19 13:07 7.file
    -rw-r--r-- 1 root root 24 May 19 13:07 8.file
    -rw-r--r-- 1 root root 24 May 19 13:07 9.file
    drwx------ 3 root root 4096 May 19 13:56 rdiff-backup-data

Now that we have backed up the original file we will run a second backup to capture changed data; this time a with a little more verbosity.

    root@backup-server:# rdiff-backup -v5 test@server.example.com::/var/tmp/backmeup /var/tmp/backups/server.example.com/
    Using rdiff-backup version 1.2.8
    Executing ssh -C test@server.example.com rdiff-backup --server
    <truncated for length>
    Backup: must_escape_dos_devices = 0
    Starting increment operation /var/tmp/backmeup to /var/tmp/backups/server.example.com
    Processing changed file .
    Incrementing mirror file /var/tmp/backups/server.example.com
    Processing changed file 1.file
    Incrementing mirror file /var/tmp/backups/server.example.com/1.file
    Processing changed file 10.file
    Incrementing mirror file /var/tmp/backups/server.example.com/10.file
    Processing changed file 2.file
    Incrementing mirror file /var/tmp/backups/server.example.com/2.file
    Processing changed file 3.file
    Incrementing mirror file /var/tmp/backups/server.example.com/3.file
    Processing changed file 4.file
    Incrementing mirror file /var/tmp/backups/server.example.com/4.file
    Processing changed file 5.file
    Incrementing mirror file /var/tmp/backups/server.example.com/5.file
    Processing changed file 6.file
    Incrementing mirror file /var/tmp/backups/server.example.com/6.file
    Processing changed file 7.file
    Incrementing mirror file /var/tmp/backups/server.example.com/7.file
    Processing changed file 8.file
    Incrementing mirror file /var/tmp/backups/server.example.com/8.file
    Processing changed file 9.file
    Incrementing mirror file /var/tmp/backups/server.example.com/9.file

As you can see `-v5` tells us what files are being processed, this is handy to see what is being backed up or being restored.

Now if we only change files 1 - 3 and run rdiff-backup again rdiff-backup should only backup files that have changed leaving the others alone.

    root@backup-server:# rdiff-backup -v5 test@server.example.com::/var/tmp/backmeup /var/tmp/backups/server.example.com/
    Using rdiff-backup version 1.2.8
    Executing ssh -C test@server.example.com rdiff-backup --server
    <truncated for length>
    Starting increment operation /var/tmp/backmeup to /var/tmp/backups/server.example.com
    Processing changed file .
    Incrementing mirror file /var/tmp/backups/server.example.com
    Processing changed file 1.file
    Incrementing mirror file /var/tmp/backups/server.example.com/1.file
    Processing changed file 2.file
    Incrementing mirror file /var/tmp/backups/server.example.com/2.file
    Processing changed file 3.file
    Incrementing mirror file /var/tmp/backups/server.example.com/3.file

If we look at the backup directory the number of files has not changed, however the contents and timestamps have.

    root@backup-server:# ls -la /var/tmp/backups/server.example.com/
    total 52
    drwxr-xr-x 3 root root 4096 May 19 13:07 .
    drwxr-xr-x 3 root root 4096 May 19 13:53 ..
    -rw-r--r-- 1 root root 76 May 19 14:10 10.file
    -rw-r--r-- 1 root root 98 May 19 14:16 1.file
    -rw-r--r-- 1 root root 98 May 19 14:16 2.file
    -rw-r--r-- 1 root root 98 May 19 14:16 3.file
    -rw-r--r-- 1 root root 73 May 19 14:10 4.file
    -rw-r--r-- 1 root root 73 May 19 14:10 5.file
    -rw-r--r-- 1 root root 73 May 19 14:10 6.file
    -rw-r--r-- 1 root root 73 May 19 14:10 7.file
    -rw-r--r-- 1 root root 73 May 19 14:10 8.file
    -rw-r--r-- 1 root root 73 May 19 14:10 9.file
    drwx------ 3 root root 4096 May 19 14:16 rdiff-backup-data

rdiff-backup will keep the current mirror unchanged and any differences will be kept in diff files within the rdiff-backup-data directory. It is not advised to modify or interact with the mirror or diff files directly, it is better to use the rdiff-backup command itself.

## Listing available backups

To see the available backups we can use `rdiff-backup -l`.

    root@backup-server:# rdiff-backup -l /var/tmp/backups/server.example.com/
    Found 5 increments:
     increments.2013-05-19T13:56:57-07:00.dir Sun May 19 13:56:57 2013
     increments.2013-05-19T14:09:52-07:00.dir Sun May 19 14:09:52 2013
     increments.2013-05-19T14:11:29-07:00.dir Sun May 19 14:11:29 2013
     increments.2013-05-19T14:16:44-07:00.dir Sun May 19 14:16:44 2013
     increments.2013-05-19T14:29:38-07:00.dir Sun May 19 14:29:38 2013
    Current mirror: Sun May 19 14:30:20 2013

If a file has been deleted and rdiff-backup has ran since the file deletion you may not find the file in the directory, you can still however list the available backups for that file by specifying it as if it did exist.

     root@backup-server:# rdiff-backup -l /var/tmp/backups/server.example.com/1.file
    Found 4 increments:
     1.file.2013-05-19T13:56:57-07:00.diff.gz Sun May 19 13:56:57 2013
     1.file.2013-05-19T14:09:52-07:00.diff.gz Sun May 19 14:09:52 2013
     1.file.2013-05-19T14:11:29-07:00.diff.gz Sun May 19 14:11:29 2013
     1.file.2013-05-19T14:16:44-07:00.snapshot.gz Sun May 19 14:16:44 2013
    Current mirror: Sun May 19 14:30:20 2013

## Restoring backed up files and directories

rdiff-backup has the ability to restore either individual files or entire directories, as long as rdiff-backup has the item within its incremental lists.

#### Restoring an individual file

When restoring an individual file with rdiff-backup you can either specify a time or the incremental file to restore from. For the following example I will show using the incremental file.

    root@backup-server:# cd server.example.com/rdiff-backup-data/increments/
    root@backup-server:# rdiff-backup -v5 1.file.2013-05-19T14:11:29-07:00.diff.gz test@server.example.com::/var/tmp/backmeup/1.file

#### Restoring a directory

When restoring a directory however we will need to specify a specific time that we want to restore to.

    root@backup-server:# rdiff-backup -v5 -r 1h server.example.com/ test@server.example.com::/var/tmp/backmeup

This command will restore the entire directory to where it was 1 hour ago or best it can depending on the backups available. rdiff-backup can support many time frames but I commonly find myself using the xDays format (e.g. 2D for 2 days).

#### Don't use the force flag

While the above command will restore the whole directory it will only do so if the directory is empty. If the directory has files in it and you ask rdiff-backup to restore that directory than it will try to remove the existing files in order to match your backup. This action could result in data that has not been backed up being removed.

To protect against accidental deletion rdiff-backup requires the **force** flag to be used anytime a file is being overwritten or deleted.

    root@backup-server:# rdiff-backup -v5 -r 1h server.example.com/ test@server.example.com::/var/tmp/backmeup
    Using rdiff-backup version 1.2.8
    Executing ssh -C server.example.com rdiff-backup --server
    Fatal Error: Restore target /var/tmp/backmeup already exists, specify --force to overwrite.

I advise avoiding the use of the **force** flag whenever possible, if you truly do not want the contents of the directory than just remove them manually before restoring. I have seen many times where people used the **force** flag and accidentally overwrote a directory they did not mean (like /etc/ for example...).

#### Restoring to another location

When restoring with rdiff-backup you can restore files or directories to a location other than their originating source. This can be handy if you need to check the contents before completely restoring the file.

    root@backup-server:# rdiff-backup -v5 -r 3h server.example.com/1.file test@server.example.com::/var/tmp/backmeup/1.file.restore

## Backup Retention

Backups are only as good as their retention period, without a retention period you will eventually run out of disk space or use far more disk space than you had originally planned. rdiff-backup has the ability to maintain a certain number of incremental copies. With rdiff-backup you can tell it to either keep a backup for a certain amount of time or for a certain number of backups.

**On backup-server:**

#### Time method

The time method uses the same time format as restore.

    root@backup-server:# rdiff-backup --force --remove-older-than 4h /var/tmp/backups/server.example.com

#### Number of backups method

To specify a number of backups use the number followed by a capital B.

    root@backup-server:# rdiff-backup --force --remove-older-than 4B /var/tmp/backups/server.example.com

I used the **force** flag with the above commands as rdiff-backup requires **force** to be given if you are removing more than one incremental copy.

## Providing more access with sudo

So far we have been backing up files and directories that the test user has access to; if we were to try and backup or restore a file that the test user does not have access to than the backup/restore will fail with a permission denied. To provide greater access you can either run rdiff-backup as the root user on the remote systems (which raises security concerns), or provide the test user with the ability to run rdiff-backup as the root user via sudo.

**Example of permission denied error:**

    root@backup-server:# rdiff-backup -v5 test@server.example.com::/var/tmp/backmeup /var/tmp/backups/server.example.com
    Using rdiff-backup version 1.2.8
    Executing ssh -C test@server.example.com rdiff-backup --server
    Exception '[Errno 13] Permission denied: '/var/tmp/backmeup'' raised of class '<type 'exceptions.OSError'>':

#### Adding the rdiff-backup into /etc/sudoers

In order to allow the test user the ability to run rdiff-backup as root we need to add an entry into the `/etc/sudoers` file, which controls what commands users can run via sudo. To modify this file we will use the visudo command.

**On server:**

    root@server:/var/tmp# visudo

**Append:**

    ## Give test user the ability to run rdiff-backup
    test ALL = NOPASSWD: /usr/bin/rdiff-backup --server

As the test user you will now see rdiff-backup in the list of available sudo commands

    test@server:~$ sudo -l
    User test may run the following commands on this host:
     (root) NOPASSWD: /usr/bin/rdiff-backup --server

We are specifying **NOPASSWD** as by default sudo would normally ask the user for their password, which would not work very well with an automated backup script.

#### Running rdiff-backup with remote-schema

In order for rdiff-backup to use sudo we will need to change the command we have been using a bit; we will use the `--remote-schema` flag to tell rdiff-backup to run `sudo /usr/bin/rdiff-backup --server` on the remote system.

**On backup-server:**

**Backup command**

    root@backup-server:# rdiff-backup -v5 --remote-schema 'ssh -C %s "sudo /usr/bin/rdiff-backup --server"' 
    test@server.example.com::/var/tmp/backmeup /var/tmp/backups/server.example.com
    <truncated>
    Processing changed file 9.file
    Incrementing mirror file /var/tmp/backups/server.example.com/9.file

**Restore command**

    root@backup-server:# rdiff-backup -v5 -r 3h --remote-schema 'ssh -C %s "sudo /usr/bin/rdiff-backup --server"' 
    /var/tmp/backups/server.example.com/5.file test@server.example.com::/var/tmp/backmeup/5.file

By adding sudo we are allowing the test user to backup and restore any file on the system with rdiff-backup.

## Adding restrict-read-only for even more security

While using rdiff-backup with sudo prevents people from using the SSH key to login as root to all of our remote systems. This solution by itself does not restrict someone from using rdiff-backups restore function from deploying compromised files.

For even more security we can use the `--restrict-read-only` flag to restrict rdiff-backup to only being able to read files and blocking all write requests. The down side of this setting is that it also prevents valid restore requests as well. If you are more worried about someone accessing your systems than having to edit the sudoers file every time you want to restore a file; than this is a good option.

#### Adding restrict-read-only to the sudoers entry

In order to add `--restrict-read-only` we need to add it to both the rdiff-backup command and the sudoers entry.

    root@server# visudo

**Modify to:**

    test ALL = NOPASSWD: /usr/bin/rdiff-backup --server --restrict-read-only /

The `/` at the end is the path that you want rdiff-backup to be restricted to. This entry would give rdiff-backup the ability to backup all files on the system. If you are not backing up the entire system you can restrict this to a specific path as well to prevent rdiff-backup from reading other files on the system not within your path.

#### Running the backup command with restrict-read-only

Now that sudo allows us to run the full command we can add it to the remote-schema.

    root@backup-server:# rdiff-backup -v5 --remote-schema 'ssh -C %s "sudo /usr/bin/rdiff-backup --server --restrict-read-only /"' 
     test@server.example.com::/var/tmp/backmeup /var/tmp/backups/server.example.com
    Using rdiff-backup version 1.2.8
    Executing ssh -C test@server.example.com "sudo /usr/bin/rdiff-backup --server"

If you modified the path in the sudoers file you would need to do the same with the rdiff-backup command above.

## Automating with Cron

Automating rdiff-backup with cron is as simple as tossing the commands above into a script and adding it to the crontab. The below is meant only for example, I would advise anyone reading this to script in some more intelligence to handle failed backups and concurrent runs but if you needed something quick and dirty this would work.

**On backup-server:**

#### Creating the backup script

    root@backup-server# vi /root/backup-example.sh

**Add:**

    #!/bin/bash
    ## Example rdiff-backup script - http://bencane.com
    ## This is not fancy, and you should really add error checking

    # Backup
    rdiff-backup -v5 --remote-schema 'ssh -C %s "sudo /usr/bin/rdiff-backup --server --restrict-read-only /"' 
    test@server.example.com::/var/tmp/backmeup /var/tmp/backups/server.example.com

    # Clean Increments
    rdiff-backup --force --remove-older-than 4B /var/tmp/backups/server.example.com

#### Adding to crontab

Once you have the script you can simply add the script into the crontab on the **backup-server**.

    root@backup-server# crontab -e

**Append:**

    # m h dom mon dow command
    0 0 * * * /root/backup-example.sh > /dev/null 2>&1

The above crontab entry will run backup-example.sh every night at midnight. This will provide you with 4 days of incremental copies at all times.

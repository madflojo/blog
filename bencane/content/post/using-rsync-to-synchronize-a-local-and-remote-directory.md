---
authors:
- Benjamin Cane
categories:
- Linux
- rsync
date: '2014-01-07T08:00:00'
description: An introduction to rsync and instructions on how to setup an automated
  rsync copy between two hosts
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- redhat
- rsync
- centos
- ubuntu
- debian
- linux copy files
- copy large files in linux
title: Using rsync to synchronize a local and remote directory
url: /2014/01/07/using-rsync-to-synchronize-a-local-and-remote-directory

---

Recently I had moved my blog from WordPress to a custom python script that generates static HTML pages. After generating files I need to copy them to my web servers. While it is easy enough to FTP or SCP the files from my local machine to the remote web servers. I am looking for a little more elegant and automated solution. For that reason I have chosen to use the `rsync` command. 

## What is rsync

In the simplest terms `rsync` is a tool that copies files from one place to another.

In a more detailed explanation `rsync` does more than just copy files, it will read the source and destination directories and only copy the files that are new or updated. This makes `rsync` perfect for copying my HTML files; as not every file will be changed.

The fact that `rsync` only copies new or updated files also makes `rsync` a great option for cases where there is a large and active directory. Recently I had to copy a multi terabyte file system from one server to another. The only problem was that file system was extremely active. Even though the copy took a long time to complete, I was able to use `rsync` to single out and copy only the changed files.

The following will outline setting up a cronjob that uses `rsync` to keep two directories synchronized.

## Installing rsync

On most systems `rsync` is installed by default, if `rsync` is not installed it can be installed with `apt-get` or `yum`.

    # apt-get install rsync

## Create an SSH Key

While you can run `rsync` without setting up SSH keys; because we want the copy to be unattended we will need to setup SSH keys. I previously covered [how to setup SSH keys](http://bencane.com/2013/06/10/creating-ssh-keys/), so I will keep the below instructions basic. In my case I will be executing `rsync` as an unprivileged user and will need to create the SSH keys as that specific user.

    $ su - testuser
    $ ssh-keygen -t rsa
    Generating public/private rsa key pair.
    Enter file in which to save the key (/data/web/testuser/.ssh/id_rsa): 
    Created directory '/data/web/testuser/.ssh'.
    Enter passphrase (empty for no passphrase): 
    Enter same passphrase again: 
    Your identification has been saved in /data/web/testuser/.ssh/id_rsa.
    Your public key has been saved in /data/web/testuser/.ssh/id_rsa.pub.

Before we can SSH to our server without a password we will need to copy the public key to the remote server, in my case I know that there is no `.ssh` directory on the remote server already. I will be creating everything from scratch, if your remote system already has a `.ssh` directory you will need to copy the public key into the `authorized_keys` file manually.

### Make sure the Remote user has a shell

In general I always make my application users with no login shell. Since we will be copying files over SSH the user will require a login shell. The below command will change the testuser's login shell to `/bin/bash`.

    # usermod -s /bin/bash testuser

### Create the .ssh directory on the Remote Server

The below commands will create a basic `.ssh` directory and copy the local systems public key to the remote systems `authorized_keys` file. 

**On Remote Server:**

    $ mkdir .ssh
    $ chmod 700 .ssh/

**On Local Server:**

    $ scp .ssh/id_rsa.pub root@remote.example.com:~testuser/.ssh/authorized_keys

**On Remote Server:**

    # chown testuser:webusr ~testuser/.ssh/authorized_keys

### Test the SSH keys

Before moving on it is a good idea to test that the SSH keys work. You can do this by opening a simple SSH connection to the remote system from the local system.

**On Local Server**

    $ ssh remote.example.com
    Welcome to Ubuntu 12.04 LTS (GNU/Linux 3.2.0-23-virtual x86_64)

## Using rsync

Now that we can SSH to the remote host without entering a password we can use `rsync` to copy the directories.

### Testing with the dry run flag

Before going willy nilly and copying a directory and all of it's contents it is a good idea to test the `rsync` command with the `--dry-run` flag.

    $ rsync -avzr --dry-run public_html remote.example.com:~/
    < output truncated >
    public_html/js/
    public_html/js/bootstrap.js
    public_html/js/jquery-1.10.2.js
    sent 27035 bytes  received 2185 bytes  11688.00 bytes/sec
    total size is 4059365  speedup is 138.92 (DRY RUN)

While it may look like everything has copied `rsync` hasn't actually copied anything. This is great for testing the syntax of the command and making sure that the correct directories are being targeted.

### Running the rsync manually

Now that we have tested `rsync` we are ready to copy the directory for real. If you are using `rsync` to copy a large directory I highly suggest using the `screen` or `nohup` commands to leave the process running after your terminal exits.

    $ rsync -avzr public_html remote.example.com:~/
    public_html/2013/12/23/yum-plugins-verifying-packages-and-configurations-with-yum-verify/index.html
    public_html/feed/index.xml
    sent 85615 bytes  received 32456 bytes  33734.57 bytes/sec
    total size is 4059365  speedup is 34.38

Before we move on I want to break down the `-avzr` flags that were given.

  * `-a` - The `-a` or `--archive` flag puts `rsync` into archive mode which makes it retain file attributes such as permissions and ownership similar to the `tar` command.
  * `-v` - The `-v` or `--verbose` flag puts `rsync` into a verbose mode, this will make `rsync` output status of the copy.
  * `-z` - The `-z` or `--compress` flag tells `rsync` to compress files during the copy, this will save time for slow network connections.
  * `-r` - The `-r` or `--recursive`  flag tells `rsync` to recursively copy files and directories.

### Using the delete flag to remove old files
 
`rsync` has the ability to remove files that are on the destination directory but not the source directory. This can be very helpful in my case as I may remove an HTML file from time to time from my source directories and do not want to be bothered having to remove it on each web server. This can also be helpful if you are setting up `rsync` to copy a large and active directory that will take several days to copy. This means you can run `rsync` a second time and remove any unneeded files. To enable this simply add the `--delete` flag to the `rsync` command.
    
    $ rsync -avzr --delete public_html remote.example.com:~/
    sending incremental file list
    public_html/
    deleting public_html/html
    deleting public_html/1.txt
    sent 25230 bytes  received 376 bytes  10242.40 bytes/sec
    total size is 4059365  speedup is 158.53

## Setup an rsync cronjob

Now that the `rsync` command is tested and we know that we can login to the remote server without user input; we can now place our command into a cronjob. This will allow us to run an `rysnc` command at a scheduled interval throughout the day.

    $ crontab -e

**Append**

    */0 * * * * /usr/bin/rsync -avzr --delete /data/web/testuser/public_html remote.example.com:/data/web/testuser/ > /dev/null 2>&1

The above example will execute the `rsync` command every hour, while this is good for a directory with a little bit of data this would not work very well for a directory with ton's of data. If you are running `rsync` to copy large amounts of data it may be better to create a wrapper script or [use this one](https://github.com/madflojo/rsync-cron-wrapper) to ensure that other `rsync` jobs aren't already running.

`rsync` is a great tool to use when you want to mirror any directory to another system. There are a ton of options that give you great flexibility to change the way `rsync` copies files and what it does with the files once they are copied.

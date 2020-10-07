---
authors:
- Benjamin Cane
categories:
- All Articles
- Applications
- File Systems
- How To and Tutorials
- NFS
date: '2012-11-23T14:30:04'
draft: false
header:
  caption: ''
  image: ''
tags:
- all
- apt-get
- chkconfig
- debian
- init
- linux
- linux distributions
- linux os
- local file system
- network file system
- nfs
- nfs server
- protocol
- red hat os
- security
- server packages
- ubuntu
title: 'NFS: Setting up a basic NFS file system share'
url: /2012/11/23/nfs-setting-up-a-basic-nfs-file-system-share

---

While there are many distributed file systems out there; especially with the rise of cloud & virtual computing. The Network File System or NFS protocol has by far held its title as an easy to use, fast to implement and very efficient distributed file system. In today's article I will be covering how to set up a basic NFS share.

This article will assume that you have already created a file system, if not hop over to [this article](http://bencane.com/2011/12/creating-a-new-filesystem-with-fdisk-lvm-and-mkfs/) and then come back for the NFS steps.

## Setting up the NFS Server

Note: The following instructions are for Ubuntu Server and can be applied to other Linux Distributions however some steps may differ such as start-up configuration.

NFS is a very simple setup. We will first configure the NFS "server" to share one of its local file systems. The local file system that we will be sharing today is `/nfs`.

**Create a test file on the NFS "server" for validation later:**

To validate that we are able to see the shared file system we will create a test file.
     
     root@server:/# echo "Test File on NFS Server" > /nfs/testfile.txt

### Install NFS Server Packages

**Verify the packages are installed:**

Now that our directory is ready we will start by ensuring that we have the appropriate packages.
     
     root@server:~$ dpkg --list | grep nfs
     ii libnfsidmap2 0.25-1ubuntu2 NFS idmapping library
     ii nfs-common 1:1.2.5-3ubuntu3.1 NFS support files common to client and server

As you can see we have some NFS packages installed however we are missing the package necessary for this system to act as an NFS Server (nfs-kernel-server).

**Install nfs-kernel-server:**

To install the nfs server package we will use `apt-get`.
     
     root@server:~$ apt-get install nfs-kernel-server

Now that the nfs server package is installed we will verify that the init script is set to start by default.

**Check your current runlevel:**
     
     root@server:/# runlevel
     N 2

**Check if the rc.d directory is linked:**
     
     root@server:/# ls -la /etc/rc2.d/ | grep nfs
     lrwxrwxrwx 1 root root 27 Aug 11 17:31 S20nfs-kernel-server -> ../init.d/nfs-kernel-server

If your output does not match above than nfs-kernel-server may not be configured to start automatically. To do this in Ubuntu/Debian you would use the `update-rc.d` command and in Red Hat variants you would use [chkconfig](http://bencane.com/2012/01/cheat-sheet-systemctl-vs-chkconfig/).

### Configure the NFS Server

With NFS we will need to configure what directories we want to be shared, to do this we will be editing the /etc/exports file.

#### NFS Configuration Syntax

For our exercise we will make sure that the /nfs directory is shared only to the client 192.168.0.195. We want this client to have read and write access and we want the nfs mount to write in synchronous mode (which is default).

The NFS exports configuration has the following syntax
     
     /directories/to/share <ip or hostname>(nfs options) (nfs options)

For our example this breaks down to
     
     /nfs 192.168.0.195/32(rw,sync)

If we wanted to share this directory with more than one client we could add an entry on the line for them as shown in the syntax area or if they are all within the same subnet we could use the appropriate CIDR address. If you know that your entire C class should have the ability to mount the NFS share you could simply do 192.168.0.0/24 and allow all IPs between 192.168.0.1-255 access to your NFS share.

#### Configure /etc/exports

Now that we have the syntax for our client configuration, lets put that configuration into the /etc/exports file.

**Edit the exports file:**
     
     root@server:~# vi /etc/exports

**Append:**
     
     /nfs 192.168.0.195/32(rw,sync)

**Refresh the exports:**
     
     root@server:~# exportfs -a

Once exportfs has finished running, the new share will be available to the clients.

## Setting up the NFS Client

### Verify if the NFS client packages are installed

Now that the server is configured let's make sure that the NFS client has the ability to mount an NFS share, to do this it will require the nfs-common package.
     
     root@client:~# dpkg --list | grep nfs
     ii libnfsidmap2 0.25-1ubuntu2 NFS idmapping library
     ii nfs-common 1:1.2.5-3ubuntu3.1 NFS support files common to client and server

By default the nfs-common package may already be installed however if it is not than it can be installed with apt-get.
     
     root@client:~# apt-get install nfs-common

### Mounting the file system

Once the nfs-common package is installed you can mount the share. However before doing so you will need to create the directory that you want the NFS file system mounted under.

#### Create the necessary path

For our tutorial we will create a `/shared/nfs1` directory and then mount the NFS share over that directory.
     
     root@client:~# mkdir -p /shared/nfs1

#### Mount the File System

When mounting an NFS file system it is best to first try mounting the file system manually and then place it into the `/etc/fstab` file. To mount it manually we will use the mount command.

**Syntax:**
     
     mount -t nfs <ip>:<remote path> <local path>

**Example:**
     
     root@client:~# mount -t nfs 192.168.0.197:/nfs /shared/nfs1

#### Validate the NFS share is mounted

To validate that our NFS is mounted we will first check if the mount command shows our newly mounted file system and second if we can access our file.
     
     root@client:~# mount
     192.168.0.197:/nfs on /shared/nfs1 type nfs (rw,vers=4,addr=192.168.0.197,clientaddr=192.168.0.195)
     
     root@client:~# cat /shared/nfs1/testfile.txt
     Test File on NFS Server

### Add the NFS share to /etc/fstab

Now that we know the mount is working we can edit the /etc/fstab file to ensure that the file system is mounted on reboot. NFS has a specific syntax required in order to mount properly, below is the syntax breakdown required for /etc/fstab.

**Syntax**
     
     <ip>:<path>    nfs  defaults, 0  0

**Example:**
     
     root@client:~# vi /etc/fstab

**Append:**
     
     192.168.0.197:/nfs nfs defaults 0 0

#### Testing your syntax

Rather than testing this by rebooting it is a bit safer to unmount the nfs share and remount it with `mount -a`. If there is an error in your `/etc/fstab` and you reboot your system the system may not complete its boot until you resolve the error. This could be difficult if the system is remote and you do not have physical access to the machine.

**Example:**
     
     root@client:~# umount /shared/nfs1
     root@client:~# mount -a
     root@client:~# mount
     192.168.0.197:/nfs on /shared/nfs1 type nfs (rw,vers=4,addr=192.168.0.197,clientaddr=192.168.0.195)

If the file system mounted than you now have an NFS file system share available to your clients. Simply repeat the client process on all of the machines you want to have access to this file system.

## No Root Squash

There are many options for NFS and I want to keep this article short but effective so I am leaving out many of the various configuration items that you could do. However there is one option that is worth mentioning, `no_root_squash`. By default NFS will downgrade any files created with the root permissions to the nobody user. This is a security feature that prevents privileges from being shared unless specifically requested.

If I create a file as the root user on the client on the NFS share, by default that file is owned by the nobody user.
     
     root@client:~# touch /shared/nfs1/file2 
     root@server:/nfs# ls -la file2
      -rw-r--r-- 1 nobody nogroup 0 Nov 18 18:06 file2

Sometimes it is important to share files that are owned as root with the proper permissions, in these cases this can be done by simply adding the `no_root_squash` attribute to the `/etc/exports` configuration.

#### Adding no_root_squash

**Edit the /etc/exports file:**
     
     root@server:/nfs# vi /etc/exports

**Modify the /nfs line to:**
     
     /nfs 192.168.0.195/32(rw,sync,no_root_squash)

**Re-Export the exported file systems:**
     
     root@server:/nfs# exportfs -a

**Re-Mount the file system on the client:**
     
     root@client:~/# umount /shared/nfs1
     root@client:~/# mount -a

Now any file created by root should have root permissions.

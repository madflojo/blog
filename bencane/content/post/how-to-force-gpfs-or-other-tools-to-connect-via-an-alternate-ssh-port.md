---
authors:
- Benjamin Cane
categories:
- Applications
- File Systems
- GPFS
- How To and Tutorials
- Linux
- Unix
date: '2013-03-19T19:56:24'
description: A simple solution to force SSH clients to default to a port other than
  22
draft: false
header:
  caption: ''
  image: ''
tags:
- global parallel file system
- gpfs
- linux
- ssh
- ssh port
- sshd server
title: How to force GPFS (or other tools) to connect via an alternate ssh port
url: /2013/03/19/how-to-force-gpfs-or-other-tools-to-connect-via-an-alternate-ssh-port

---

Recently I have been playing with the Global Parallel File System, which is a clustered file system from IBM. When setting up a cluster you can configure GPFS to utilize SSH/SCP to send administrative tasks to the other nodes in the cluster.

The problem I ran into was that in my environment I do not run SSH over port 22 (for various reasons I wont get into). Needless to say once I configured SSH to listen on an alternate port GPFS stopped working.

After a bit of Googling I could not find anywhere in GPFS itself where you can specify the SSH port to connect to. All hope seemed lost, but then I remembered a little trick I learned long ago.

## Change the ssh port

When GPFS is issuing an SSH command it is simply using the ssh client to connect. The ssh client, much like the sshd server has a configuration file. Within that configuration file you can specify what port to connect to by default. In order to force GPFS to connect to an SSH server via a non-standard port you can change the port in the SSH Client configuration file. After this change all ssh client connections will default to the specified port.

Below are instructions on how to change the ssh client & server ports to port 2022 and then test to ensure GPFS can communicate with all nodes.

The below steps will need to be executed on all hosts in the GPFS cluster.

### Change the ssh server's default port

#### Edit the sshd_config file

Before changing the client configuration we need to tell the SSHD server to listen on an alternative port; we will be using port 2022 for our example.

    [allhosts ~]# vi /etc/ssh/sshd_config

**Find:**

    #Port 22

**Replace:**

    Port 2022

#### Restart SSHD

Before this change takes affect we will need to restart the SSHD service.

Before logging out open a new ssh connection to this server to validate SSHD is up and accepting connections. If it is not working, make sure you check your firewall rules.

    [allhosts ~]# /etc/init.d/sshd restart

### Change the ssh client's default port

At this point if you simply tried to type `ssh <server>` the command would fail as the client is defaulting to port 22.

    [host2 ~]# ssh host1
     ssh: connect to host host1 port 22: Connection refused
    [host2 ~]# ssh host1 -p 2022
     root@host1's password:

#### Edit the ssh_config file

In order to make the ssh client default to port 2022 we will need to edit the ssh_config file.

    [allhosts ~]# vi /etc/ssh/ssh_config

**Find:**

    # Port 22

**Replace:**

    Port 2022

### Test ssh connectivity

Now all ssh connectivity on hosts where you changed ssh_config will default to port 2022.

    [host1 ~]# ssh host2
    root@host2's password:
    [host2 ~]# ssh host1
    root@host1's password:

### Test GPFS communication

**Before SSH Change:**

    # mmgetstate -a
    Node number Node name GPFS state
     ------------------------------------------
     1 HOST1 unknown
     3 HOST3 unknown
     4 HOST2 unknown
     5 HOST4 unknown
     6 HOST5 active

**After SSH Change:**

    # mmgetstate -a
    Node number Node name GPFS state
     ------------------------------------------
     1 HOST1 active
     3 HOST3 active
     4 HOST2 active
     5 HOST4 active
     6 HOST5 active

### Additional notes

While the above examples are geared for GPFS this concept can be applied to any service that uses ssh to communicate that also uses the servers ssh client. This method would not apply to any applications that use their own ssh client implementation.

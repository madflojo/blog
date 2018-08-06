---
authors:
- Benjamin Cane
categories:
- How To and Tutorials
- Linux
- Security
- SysAdmin Basics
- Unix
date: '2013-06-10T12:00:33'
description: A how to on generating SSH Private and Public keys and using them for
  passphrase less logins
draft: false
header:
  caption: ''
  image: ''
tags:
- all
- linux
- linux os
- private keys
- public keys
- red hat
- red hat os
- ssh
- ssh servers
- ubuntu
title: 'ssh-keygen: Creating SSH Private/Public Keys'
url: /2013/06/10/creating-ssh-keys

---

Are you tired of trying to memorize tons of passwords on different systems? Or do you simply want to have a faceless user SSH between two systems without being asked for a password? Well you are in luck because today we will be covering SSH keys.

SSH Servers have the ability to authenticate users using public/private keys. In the case of pass-phrase less keys this allows users to ssh from one system to another without typing a password.

This is great for faceless users or any lazy "people" users that don't feel like typing in their passwords when they connect to systems over ssh.

## Generate the Private and Public Keys

To generate the SSH keys we will be using the ssh-keygen command. This command will generate an RSA public and private key. The ssh-keygen command will also support DSA keys. I will leave the discussion of RSA vs DSA for [other places](http://security.stackexchange.com/questions/5096/rsa-vs-dsa-for-ssh-authentication-keys).

    madflojo@local-server:~$ ssh-keygen -t rsa
    Generating public/private rsa key pair.
    Enter file in which to save the key (/home/madflojo/.ssh/id_rsa):
    Created directory '/home/madflojo/.ssh'.
    Enter passphrase (empty for no passphrase):
    Enter same passphrase again:
    Your identification has been saved in /home/madflojo/.ssh/id_rsa.
    Your public key has been saved in /home/madflojo/.ssh/id_rsa.pub.
    The key fingerprint is:

When run `ssh-keygen` will create a directory `.ssh`,as well as two files `.ssh/id_rsa` and `.ssh/id_rsa.pub`. The first file `id_rsa` is the **private key** that will stay only on the local system, that we will authenticate from. The second file `id_rsa.pub` is the **public key** and the contents of this key will be dispersed to a remote system for key based authentication.

## Configure the Remote Server

#### Creating a .ssh directory

On the remote system you may and may not already have a .ssh directory; if it already exists you can skip this step.

    madflojo@remote-server:~# mkdir .ssh
    madflojo@remote-server:~#chmod 700 .ssh
    madflojo@remote-server:~#chown youruser:yourgroup .ssh

Pay close attention to the permissions on this directory. **Key based authentication will not work if the permissions on the .ssh directory are not correct.**

#### Append the public key to the authorized_keys file

Now that the directory is created we will put the public key information into the authorized_keys file on the remote system.

The below instructions are on two different systems so pay attention to the hostname.

    madflojo@local-server:~# cat .ssh/id_rsa.pub
    Copy the output

    madflojo@remote-server:~$ vi .ssh/authorized_keys
    Append the public key

At this point you should be able to ssh from **local-server** to **remote-server** using your ssh keys to authenticate.

    madflojo@local-server:~# ssh madflojo@remote-server
    madflojo@remote-server:~#

## Troubleshooting

#### Check the appropriate log files

If key based authentication is not working the best place to start troubleshooting is the log files. For **Debian/Ubuntu** based distributions the authentication logs are in `/var/log/auth.log`. For **Red Hat** based distributions the authentication logs are in `/var/log/secure`.

Usually, I find it is due to permissions on the .ssh directory.

#### Check the sshd_config file

On most Linux distributions SSH servers have Public Key Authentication enabled by default. If you are having problems getting this to work make sure you un-comment the below lines in the `sshd_config` file.

    # vi /etc/ssh/sshd_config
    RSAAuthentication yes
    PubkeyAuthentication yes
    AuthorizedKeysFile %h/.ssh/authorized_keys

The `AuthorizedKeysFile` line may be different depending on your distribution but it should be pointing to `.ssh/authorized_keys` in the users home directory.

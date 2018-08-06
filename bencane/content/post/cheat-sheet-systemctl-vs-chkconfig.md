---
authors:
- Benjamin Cane
categories:
- Cheat Sheets
- Linux
- Linux Commands
- Linux Distributions
- Red Hat
date: '2012-01-19T15:20:54'
description: A simple cheat sheet that shows how to perform the same task with both
  systemctl and chkconfig
draft: false
header:
  caption: ''
  image: ''
tags:
- chkconfig
- linkedin
- linux
- systemctl
- systemd
- tech
title: 'Cheat Sheet: systemctl vs chkconfig'
url: /2012/01/19/cheat-sheet-systemctl-vs-chkconfig

---

Since I've mostly been using Red Hat or the gui desktop of Ubuntu lately I've neglected to notice the transitions from the sysVinit packages to systemd. Recently I installed Fedora 16 and was a little surprised when chkconfig didn't work anymore. I decided I would write a post that gives the systemctl version of a few common chkconfig commands.

## List processes

**chkconfig**:

    # chkconfig --list

**systemd**:

    # systemctl list-units

## Enable a service

**chkconfig**:

    # chkconfig <servicename> on

**systemd**:

    # systemctl enable <servicename>.service

## Disable a service

**chkconfig**:

    # chkconfig <servicename> off

**systemd**:

    # systemctl disable <servicename>.service

## Start a service

**chkconfig**:

    # service <servicename> start

**systemd**:

    # systemctl start <servicename>.service

## Stop a service

**chkconfig**:

    # service <servicename> stop

**systemd**:

    # systemctl stop <servicename>.service

### Check the status of a service

**chkconfig**:

    # service <servicename> status

**systemd**:

    # systemctl status <servicename>.service

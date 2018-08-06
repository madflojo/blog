---
authors:
- Benjamin Cane
categories:
- How To and Tutorials
- Linux
- Linux Commands
date: '2012-07-16T15:00:53'
draft: false
header:
  caption: ''
  image: ''
tags:
- iproute
- kernel
- linkedin
- linux
- linux os
- netem
- network
- network latency
- ping
- qdisc
- servers
- tc
- tc command
- WAN
- wide area network
title: Adding simulated network latency to your Linux server
url: /2012/07/16/tc-adding-simulated-network-latency-to-your-linux-server

---

Have you ever said to yourself, "man I really need to slow down my internet"?

Probably not very often, but recently I found myself in a dilemma where I needed to simulate 120ms of network latency in my test environment which consists of servers that are racked right next to each other. That is where the command `tc` comes in.

Within the current distributions of Linux there is a kernel component called netem, which adds Network Emulation and is used for testing and simulating the same types of issues one would see in a WAN (Wide Area Network). `tc` Is a command that allows one to add rules to netem, specifically we will cover how to add network latency on a specific device with tc.

### Installation

The tc command ships with the iproute package which is installed by default; we will not need to install any packages to use tc.

### Adding Latency

The tc command will add the amount of latency specified, in order to simulate the same rate of latency as my production environment I will need to take my desired latency and subtract my test targets latency to figure out the amount of latency I need netem to add.
     
     "Production Target Latency" - "Test Target Latency" = "Latency to Add via netem"

In order to determine the latency of your test target you can perform a simple ping and use the ping's round-trip time to determine your networks latency. In this case google.com will be our test target.
     
     # ping google.com
      PING google.com (74.125.224.230) 56(84) bytes of data.
      64 bytes from lax04s08-in-f6.1e100.net (74.125.224.230): icmp_req=1 ttl=56 time=24.1 ms
      64 bytes from lax04s08-in-f6.1e100.net (74.125.224.230): icmp_req=2 ttl=56 time=24.2 ms
      64 bytes from lax04s08-in-f6.1e100.net (74.125.224.230): icmp_req=3 ttl=56 time=21.9 ms

My average latency to google.com is 23.6ms in order to get 120ms of latency I need to add 96.6ms, for ease of use I will round-up to 97.
     
     # tc qdisc add dev eth0 root netem delay 97ms

To verify the command set the rule run `tc -s`.
     
     # tc -s qdisc
     qdisc netem 8002: dev eth0 root refcnt 2 limit 1000 delay 97.0ms

As you can see the 97ms delay rule has been added to netem, now we test with another ping.
     
     # ping google.com
     PING google.com (74.125.239.8) 56(84) bytes of data.
     64 bytes from lax04s09-in-f8.1e100.net (74.125.239.8): icmp_req=1 ttl=56 time=122 ms
     64 bytes from lax04s09-in-f8.1e100.net (74.125.239.8): icmp_req=2 ttl=56 time=120 ms
     64 bytes from lax04s09-in-f8.1e100.net (74.125.239.8): icmp_req=3 ttl=56 time=120 ms

Now my round-trip ping time is taking 120ms.

Note: Because you are adding this rule to a specific interface all traffic out of that interface will have the 97ms delay.

### Remove the rule

After you have completed testing you can remove the delay with the tc command as well.
     
     # tc qdisc del dev eth0 root netem
     # tc -s qdisc
     qdisc pfifo_fast 0: dev eth0 root refcnt 2 bands 3 priomap 1 2 2 2 1 2 0 0 1 1 1 1 1 1 1 1

These settings will not survive a reboot, be sure to check your netem rules after any reboot.

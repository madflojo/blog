---
authors:
- Benjamin Cane
categories:
- How To and Tutorials
- Linux
- Linux Commands
- Linux Distributions
- Networking
- Red Hat
- Troubleshooting
date: '2013-05-12T00:44:01'
description: Walkthrough on what Static Routes are and how to add them on Red Hat
  based Linux Distributions
draft: false
header:
  caption: ''
  image: ''
tags:
- default route
- ip command
- ip route
- linux
- linux distributions
- linux os
- network
- network communication
- network configuration
- red hat
- red hat os
- route
- routing table
- static routes
- troubleshooting
- WAN
title: Adding and Troubleshooting Static Routes on Red Hat based Linux Distributions
url: /2013/05/12/adding-and-troubleshooting-static-routes-on-red-hat-based-linux-distributions

---

Adding static routes in Linux can be troublesome, but also absolutely necessary depending on your network configuration. I call static routes troublesome because they can often be the cause of long troubleshooting sessions wondering why one server can't connect to another.

This is especially true when dealing with teams that may not fully understand or know the remote servers IP configuration.

## The Default Route

Linux, like any other OS has a routing table that determines what is the next hop for every packet.

#### Print the routing table contents

There are numerous commands that show the routing table but today we will use the `ip` command as this command will be replacing the `route` command in future releases.

    # ip route show
     10.1.6.0/26 dev eth0 proto kernel scope link src 10.1.6.21
     10.1.7.0/24 dev eth1 proto kernel scope link src 10.1.7.41
     default via 10.1.6.1 dev eth0

As you can see in the example routing table there are numerous routes however 1 route shows as the **default route**. This routing table tells the system that if the IP that is being communicated to does not fall into any of the other routes than send the packets to the default route defined as **10.1.6.1**. The default route basically acts as a catchall for any packet that isn't being told what to do in the above routes.

## Our Example System

In today's article I will be referencing an example network configuration in order to show how static routes are added, why to add them and some basic troubleshooting.

#### Example Interface Configuration

**eth0:**

    # cat /etc/sysconfig/network-scripts/ifcfg-eth0
    DEVICE=eth0
    BOOTPROTO=static
    IPADDR=10.1.6.21
    NETMASK=255.255.255.192
    ONBOOT=yes

**eth1:**

    # cat /etc/sysconfig/network-scripts/ifcfg-eth1
    DEVICE=eth1
    BOOTPROTO=static
    IPADDR=10.1.7.41
    NETMASK=255.255.255.0
    ONBOOT=yes

#### Example Default Route Configuration

    # cat /etc/sysconfig/network
    NETWORKING=yes
    HOSTNAME=testing.example.com
    GATEWAY=10.1.6.1

The `GATEWAY` configuration in `/etc/sysconfig/network` tells the system that **10.1.6.1** is the **default route**. This configuration could also be added to `/etc/sysconfig/network-scripts/ifcfg-eth0` file; However if multiple `ifcfg-<interface>` files have a `GATEWAY` this may provide unexpected results as there can only be one default route.

#### Example Why we need a static route

For our example network configuration we have two interfaces; **eth0 (10.1.6.21)** for the internet, and **eth1 (10.1.7.41)** for the internal network. If we were to hook up to a backup server such as **10.1.5.202** we would want the connectivity to go through **eth1** the **internal network**, rather than **eth0** which is the **internet network**.

Since **10.1.5.202** is not in the same subnet at **eth1 (10.1.7.0/24)** the routing table does not automatically route the packet through **eth1** and would then hit the "catchall" default route out **eth0**. To force all of our packets destined for **10.1.5.202** out **eth1** we will need to set up a static route.

## Adding a Static Route

#### Adding the route to the current routing table

Adding the static route is a fairly simple task however before we start we must first know the gateway for the internal network; for our example the gateway is **10.1.7.1**.

##### Adding a single IP

    # ip route add 10.1.5.202/32 via 10.1.7.1 dev eth1

The above command adds a route that tells the system to send all packets for **10.1.5.202** and only that IP to **10.1.7.1** from device **eth1**.

##### Adding a subnet of IP's

In order to add a whole subnet than you will need to change the CIDR on the end of the IP. In this case I want to add anything in the **10.1.5.0 - 10.1.5.255** IP range. To do that I can specify the netmask of **255.255.255.0** in [CIDR format](http://wiki.samat.org/CheatSheet/IPv4CIDRNotation)**(/24)** at the end of the IP itself.

If a CIDR (or netmask) is not specified the route will default to a /32 (single ip) route.

    # ip route add 10.1.5.0/24 via 10.1.7.1 dev eth1

The difference between these two routes is that the second will route anything between **10.1.5.0** and **10.1.5.255** out** eth1** with 1 route command. This is useful if you need to communicate with multiple servers in a network and don't want to manage lengthy routing tables.

#### Adding the route even after a network restart

While the commands above added the static route they are only in the routing table until either the server or network service is restarted. In order to add the route permanently, the route can be added to the `route-<interface>` file.

    # vi /etc/sysconfig/network-scripts/route-eth1

**Append:**

    10.1.5.0/24 via 10.1.7.1 dev eth1

If the above configuration file does not already exist than simply create it and put only the route itself in the file (# comments are ok). When the interface is restarted next the system will add any valid route in the `route-eth1` file to the routing table.

I highly suggest that when possible anytime you add a route to the `route-<interface>` files that the interface itself is restarted to validate whether the route is actually in place correctly or not. I have been on many late night calls where a static route was not added correctly to the configuration files and was removed on the next reboot, which is also long after everyone has forgotten that a static route was required.

## Troubleshooting a Static Route

#### Check if the route is in the routing table

Before performing any deep down troubleshooting steps the easiest and first step should be to check if the routing table actually has the route you expect it to have.

    # ip route show
     10.1.5.0/24 via 10.1.7.1 dev eth1
     10.1.6.0/26 dev eth0 proto kernel scope link src 10.1.6.21
     10.1.7.0/24 dev eth1 proto kernel scope link src 10.1.7.41
     default via 10.1.6.1 dev eth0

#### Use tcpdump to see tcp/ip communication

The easiest way that I have found to find out whether a static route is working correctly or not is to use `tcpdump` to look at the network communication. In our example above we were attempting to communicate to **10.1.5.202** through device **eth1**.

    # tcpdump -qnnvvv -i eth1 host 10.1.5.202
    tcpdump: listening on eth1, link-type EN10MB (Ethernet), capture size 96 bytes
    16:50:35.880941 IP (tos 0x10, ttl 64, id 59563, offset 0, flags [DF], proto: TCP (6), length: 60) 10.1.7.41.41403 > 10.1.5.202.22: tcp 0
    16:50:35.881266 IP (tos 0x0, ttl 59, id 0, offset 0, flags [DF], proto: TCP (6), length: 60) 10.1.5.202.22 > 10.1.7.41.41403: tcp 0

The above `tcpdump` command will only listen on **eth1** and output only results that to or from **10.1.5.202**.

TCP connections require communication from both the source and the destination, to validate a static route you can simply initiate a tcp connection (telnet to port 22 in this case) from the server with the static route to the destination server. In the output above you can see communication from **10.1.7.41** to **10.1.5.202** from the **eth1** interface, this line alone shows that the static route is working correctly.

If the static route was incorrect or missing the tcpdump output would look similar to the following.

    # tcpdump -qnnvvv -i eth1 host 10.1.5.202
    tcpdump: listening on eth1, link-type EN10MB (Ethernet), capture size 96 bytes
    16:50:35.881266 IP (tos 0x0, ttl 59, id 0, offset 0, flags [DF], proto: TCP (6), length: 60) 10.1.5.202.22500 > 10.1.7.41.22: tcp 0

In the above, only the target server is communicating over **eth1**.

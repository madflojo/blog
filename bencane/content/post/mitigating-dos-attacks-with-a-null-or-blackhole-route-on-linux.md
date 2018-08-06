---
authors:
- Benjamin Cane
categories:
- Administration
- Best Practices
- Linux
- Linux Commands
- Networking
- Security
date: '2013-01-14T13:15:03'
description: A guide on how to lessen the damage of a DoS attack by using a null route
  in Linux
draft: false
header:
  caption: ''
  image: ''
tags:
- black hole
- ddos attacks
- denial of service
- denial of service attacks
- firewall
- ip route
- iptables
- linux
- linux firewall
- network
- network communication
- null route
- route
- routing table
- tech
- unix
title: Mitigating DoS Attacks with a null (or Blackhole) Route on Linux
url: /2013/01/14/mitigating-dos-attacks-with-a-null-or-blackhole-route-on-linux

---

In a world where the Anonymous group is petitioning the US Government to make DDoS attacks a legal means of protest; For internet facing systems the threat of Denial of Service attacks are very real.

The cold harsh reality of DoS attacks are that there is no way to stop them. While there are services out there that are designed to take the brunt of the attack for you these costs a significant amount of money (update: [CloudFlare](https://www.cloudflare.com/) seems pretty decent). A small firms only choice when faced with a DoS attack is to simply ride through the attack with the least amount of damage possible.

On a Linux/Unix system you can mitigate the effects of an attack by blocking the communication with the attacking ip addresses. You can either do this by creating [IPTables Rules](http://bencane.com/2012/09/iptables-linux-firewall-rules-for-a-basic-web-server/) or via a null route also known as a black-hole route.

## Which is better null routes or IPTables rules?

The question of which is better NULL Routes or IPTables rules can be better described as "Which is more efficient for the system to traverse the iptables rule set or the routing table". This is somewhat going to depend on the system in question. If you have a system with thousands of routes defined in the routing table and nothing in the iptables rules than it might actually be more efficient to input an iptables rule.

In most systems however the routing table is fairly small, in cases like this it is actually more efficient to use null routes. This is especially true if you already have extensive iptables rules in place.

## How to null routes work

When you define a route on a Linux/Unix system it tells the system in order to communicate with the specified IP address you will need to route your network communication to this specific place.

When you define a null route it simply tells the system to drop the network communication that is designated to the specified IP address. What this means is any TCP based network communication will not be able to be established as your server will no longer be able to send an SYN/ACK reply. Any UDP based network communication however will still be received; however your system will no longer send any response to the originating IP.

In less technical terms this means your system will receive data from the attackers but no longer respond to it.

## Adding and Removing a null route

### How to add a null route

In our example we are receiving unwanted SSH login attempts from 192.168.0.195
     
     root@server:~# netstat -na | grep :22
     tcp 0 0 0.0.0.0:22 0.0.0.0:* LISTEN
     tcp 0 0 192.168.0.197:22 192.168.0.195:57776 ESTABLISHED

To add the null route we will use the `ip` command
     
     root@server:~# ip route add blackhole 192.168.0.195/32

To verify the route is in place will will use `ip route show`
     
     root@server:~# ip route show
     default via 192.168.0.1 dev eth0 metric 100
     blackhole 192.168.0.195

After a little while the established ssh connections will time out and all subsequent connections from the blocked ip will receive the following.
     
     baduser@attacker:~$ ssh 192.168.0.197
     ssh: connect to host 192.168.0.197 port 22: No route to host

### Removing a null route

After the attack has subsided or in case you add the wrong ip you may want to remove the blackhole route. To do so we will use the `ip` command again.

     root@server:~# ip route del 192.168.0.195
     root@server:~# ip route show
     default via 192.168.0.1 dev eth0 metric 100

## Other uses for null routes

While a null route may mainly be used to mitigate DoS attacks there are some other uses. Any time you want to prevent a system from talking to another system you can simply use null routes. I have used null routes to simulate a disaster recovery scenario while testing an automated failover system many times.

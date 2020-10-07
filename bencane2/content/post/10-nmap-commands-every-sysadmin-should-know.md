---
authors:
- Benjamin Cane
categories:
- Administration
- Cheat Sheets
- Linux
- Linux Commands
- Networking
- Security
- Unix
- Unix Commands
date: '2013-02-25T18:45:41'
description: A cheat sheet list of 10 nmap commands that are extremely useful for
  every Systems or Network Administrator
draft: false
header:
  caption: ''
  image: ''
tags:
- firewall
- linux
- network
- network scanner
- network security
- nmap
- open ports
- ping
- protocol
- security
- unix
title: 10 nmap Commands Every Sysadmin Should Know
url: /2013/02/25/10-nmap-commands-every-sysadmin-should-know

---

Recently I was compiling a list of Linux commands that every sysadmin should know. One of the first commands that came to mind was nmap.

nmap is a powerful network scanner used to identify systems and services. nmap was originally developed with network security in mind, it is a tool that was designed to find vulnerabilities within a network. nmap is more than just a simple port scanner though, you can use nmap to find specific versions of services, certain OS types, or even find that pesky printer someone put on your network without telling you.

nmap can be used for good and for evil, today we will cover some common situations where nmap makes life easier for sysadmins which is generally good. Even if some Sysadmins are evil...

## Discover IP's in a subnet (no root)
     
     $ nmap -sP 192.168.0.0/24
     Starting Nmap 5.21 ( http://nmap.org ) at 2013-02-24 09:37 MST
     Nmap scan report for 192.168.0.1
     Host is up (0.0010s latency).
     Nmap scan report for 192.168.0.95
     Host is up (0.0031s latency).
     Nmap scan report for 192.168.0.110
     Host is up (0.0018s latency).

This is one of the simplest uses of nmap. This command is commonly refereed to as a "ping scan", and tells nmap to send an icmp echo request, TCP SYN to port 443, TCP ACK to port 80 and icmp timestamp request to all hosts in the specified subnet. nmap will simply return a list of ip's that responded. Unlike many nmap commands this particular one does not require root privileges, however when executed by root nmap will also by default send arp requests to the subnet.

## Scan for open ports (no root)
     
     $ nmap 192.168.0.0/24
     Starting Nmap 5.21 ( http://nmap.org ) at 2013-02-24 09:23 MST
     Nmap scan report for 192.168.0.1
     Host is up (0.0043s latency).
     Not shown: 998 closed ports
     PORT STATE SERVICE
     80/tcp open http
     443/tcp open https

This scan is the default scan for nmap and can take some time to generate. With this scan nmap will attempt a TCP SYN connection to 1000 of the most common ports as well as an icmp echo request to determine if a host is up. nmap will also perform a DNS reverse lookup on the identified ip's as this can sometimes be useful information.

## Identify the Operating System of a host (requires root)
     
     # nmap -O 192.168.0.164
     Starting Nmap 5.21 ( http://nmap.org ) at 2013-02-24 09:49 MST
     Nmap scan report for 192.168.0.164
     Host is up (0.00032s latency).
     Not shown: 996 closed ports
     PORT STATE SERVICE
     88/tcp open kerberos-sec
     139/tcp open netbios-ssn
     445/tcp open microsoft-ds
     631/tcp open ipp
     MAC Address: 00:00:00:00:00:00 (Unknown)
     Device type: general purpose
     Running: Apple Mac OS X 10.5.X
     OS details: Apple Mac OS X 10.5 - 10.6 (Leopard - Snow Leopard) (Darwin 9.0.0b5 - 10.0.0)
     Network Distance: 1 hop

With the `-O` option nmap will try to guess the targets operating system. This is accomplished by utilizing information that nmap is already getting through the TCP SYN port scan. This is usually a best guess but can actually be fairly accurate. The operating system scan however does require root privileges.

## Identify Hostnames (no root)
     
     $ nmap -sL 192.168.0.0/24
     Starting Nmap 5.21 ( http://nmap.org ) at 2013-02-24 09:59 MST
     Nmap scan report for 192.168.0.0
     Nmap scan report for router.local (192.168.0.1)
     Nmap scan report for fakehost.local (192.168.0.2)
     Nmap scan report for another.fakehost.local (192.168.0.3)

This is one of the most subtle commands of nmap, the `-sL` flag tells nmap to do a simple DNS query for the specified ip. This allows you to find hostnames for all of the ip's in a subnet without having send a packet to the individual hosts themselves.

Hostname information can tell you a lot more about a network than you would think, for instance if you labeled your Active Directory Servers with ads01.domain.com you shouldn't be surprised if someone guesses its use.

## TCP Syn and UDP Scan (requires root)
     
     # nmap -sS -sU -PN 192.168.0.164
     Starting Nmap 5.21 ( http://nmap.org ) at 2013-02-24 13:25 MST
     Nmap scan report for 192.168.0.164
     Host is up (0.00029s latency).
     Not shown: 1494 closed ports, 496 filtered ports
     PORT STATE SERVICE
     88/tcp open kerberos-sec
     139/tcp open netbios-ssn
     445/tcp open microsoft-ds
     631/tcp open ipp
     88/udp open|filtered kerberos-sec
     123/udp open ntp
     137/udp open netbios-ns
     138/udp open|filtered netbios-dgm
     631/udp open|filtered ipp
     5353/udp open zeroconf

The TCP SYN and UDP scan will take a while to generate but is fairly unobtrusive and stealthy. This command will check about 2000 common tcp and udp ports to see if they are responding. When you use the `-Pn` flag this tells nmap to skip the ping scan and assume the host is up. This can be useful when there is a firewall that might be preventing icmp replies.

## TCP SYN and UDP scan for all ports (requires root)
     
     # nmap -sS -sU -PN -p 1-65535 192.168.0.164
     Starting Nmap 5.21 ( http://nmap.org ) at 2013-02-24 10:18 MST
     Nmap scan report for 192.168.0.164
     Host is up (0.00029s latency).
     Not shown: 131052 closed ports
     PORT STATE SERVICE
     88/tcp open kerberos-sec
     139/tcp open netbios-ssn
     445/tcp open microsoft-ds
     631/tcp open ipp
     17500/tcp open unknown
     88/udp open|filtered kerberos-sec
     123/udp open ntp
     137/udp open netbios-ns
     138/udp open|filtered netbios-dgm
     631/udp open|filtered ipp
     5353/udp open zeroconf
     17500/udp open|filtered unknown
     51657/udp open|filtered unknown
     54658/udp open|filtered unknown
     56128/udp open|filtered unknown
     57798/udp open|filtered unknown
     58488/udp open|filtered unknown
     60027/udp open|filtered unknown

This command is the same as above however by specifying the full port range from 1 to 65535 nmap will scan to see if the host is listening on all available ports. You can use the port range specification on any scan that performs a port scan.

## TCP Connect Scan (no root)
     
     $ nmap -sT 192.168.0.164
     Starting Nmap 5.21 ( http://nmap.org ) at 2013-02-24 12:48 MST
     Nmap scan report for 192.168.0.164
     Host is up (0.0014s latency).
     Not shown: 964 closed ports, 32 filtered ports
     PORT STATE SERVICE
     88/tcp open kerberos-sec
     139/tcp open netbios-ssn
     445/tcp open microsoft-ds
     631/tcp open ipp

This command is similar to the TCP SYN scan however rather than sending a SYN packet and reviewing the headers it will ask the OS to establish a TCP connection to the 1000 common ports.

## Aggressively Scan Hosts (no root)
     
     $ nmap -T4 -A 192.168.0.0/24
     Nmap scan report for 192.168.0.95
     Host is up (0.00060s latency).
     Not shown: 996 closed ports
     PORT STATE SERVICE VERSION
     22/tcp open ssh OpenSSH 5.9p1 Debian 5ubuntu1 (protocol 2.0)
     | ssh-hostkey: 1024 00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:6c (DSA)
     |_2048 00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:6c (RSA)
     80/tcp open http nginx 1.1.19
     |_http-title: 403 Forbidden
     |_http-methods: No Allow or Public header in OPTIONS response (status code 405)
     111/tcp open rpcbind
     | rpcinfo:
     | program version port/proto service
     | 100000 2,3,4 111/tcp rpcbind
     | 100000 2,3,4 111/udp rpcbind
     | 100003 2,3,4 2049/tcp nfs
     | 100003 2,3,4 2049/udp nfs
     | 100005 1,2,3 46448/tcp mountd
     | 100005 1,2,3 52408/udp mountd
     | 100021 1,3,4 35394/udp nlockmgr
     | 100021 1,3,4 57150/tcp nlockmgr
     | 100024 1 49363/tcp status
     | 100024 1 51515/udp status
     | 100227 2,3 2049/tcp nfs_acl
     |_ 100227 2,3 2049/udp nfs_acl
     2049/tcp open nfs (nfs V2-4) 2-4 (rpc #100003)
     Service Info: OS: Linux; CPE: cpe:/o:linux:kernel

Unlike some of the earlier commands this command is very aggressive and very obtrusive. The `-A` simply tells nmap to perform OS checking and version checking. The `-T4` is for the speed template, these templates are what tells nmap how quickly to perform the scan. The speed template ranges from 0 for slow and stealthy to 5 for fast and obvious.

## Fast Scan (no root)
     
     $ nmap -T4 -F 192.168.0.164
     Starting Nmap 6.01 ( http://nmap.org ) at 2013-02-24 12:49 MST
     Nmap scan report for 192.168.0.164
     Host is up (0.00047s latency).
     Not shown: 96 closed ports
     PORT STATE SERVICE
     88/tcp open kerberos-sec
     139/tcp open netbios-ssn
     445/tcp open microsoft-ds
     631/tcp open ipp

This scan limits the scan to the most common 100 ports, if you simply want to know some potential hosts with ports open that shouldn't be this is a quick and dirty command to use.

## Verbose

     $ nmap -T4 -A -v 192.168.0.164
     Starting Nmap 6.01 ( http://nmap.org ) at 2013-02-24 12:50 MST
     NSE: Loaded 93 scripts for scanning.
     NSE: Script Pre-scanning.
     Initiating Ping Scan at 12:50
     Scanning 192.168.0.164 [2 ports]
     Completed Ping Scan at 12:50, 0.00s elapsed (1 total hosts)
     Initiating Parallel DNS resolution of 1 host. at 12:50
     Completed Parallel DNS resolution of 1 host. at 12:50, 0.01s elapsed
     Initiating Connect Scan at 12:50
     Scanning 192.168.0.164 [1000 ports]
     Discovered open port 139/tcp on 192.168.0.164
     Discovered open port 445/tcp on 192.168.0.164
     Discovered open port 88/tcp on 192.168.0.164
     Discovered open port 631/tcp on 192.168.0.164
     Completed Connect Scan at 12:50, 5.22s elapsed (1000 total ports)
     Initiating Service scan at 12:50
     Scanning 4 services on 192.168.0.164
     Completed Service scan at 12:51, 11.00s elapsed (4 services on 1 host)
     NSE: Script scanning 192.168.0.164.
     Initiating NSE at 12:51
     Completed NSE at 12:51, 12.11s elapsed
     Nmap scan report for 192.168.0.164
     Host is up (0.00026s latency).
     Not shown: 996 closed ports
     PORT STATE SERVICE VERSION
     88/tcp open kerberos-sec Mac OS X kerberos-sec
     139/tcp open netbios-ssn Samba smbd 3.X (workgroup: WORKGROUP)
     445/tcp open netbios-ssn Samba smbd 3.X (workgroup: WORKGROUP)
     631/tcp open ipp CUPS 1.4
     | http-methods: GET HEAD OPTIONS POST PUT
     | Potentially risky methods: PUT
     |_See http://nmap.org/nsedoc/scripts/http-methods.html
     | http-robots.txt: 1 disallowed entry
     |_/
     Service Info: OS: Mac OS X; CPE: cpe:/o:apple:mac_os_x

By adding verbose to a majority of the commands above you get a better insight into what nmap is doing; for some scans verbosity will provide additional details that the report does not provide.

While these are 10 very useful nmap commands I am sure there are some more handy nmap examples out there. If you have one to add to this list feel free to drop it into a comment.

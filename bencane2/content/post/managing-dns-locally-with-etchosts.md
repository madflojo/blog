---
authors:
- Benjamin Cane
categories:
- All Articles
- Best Practices
- How To and Tutorials
- Linux
- Networking
- SysAdmin Basics
- Troubleshooting
- Unix
date: '2013-10-29T13:27:14'
description: An article that explains what the heck the /etc/hosts file is and how
  you can use it to manage DNS locally
draft: false
header:
  caption: ''
  image: ''
tags:
- bind
- dns
- enterprise
- hosts
- linux
- linux networking
- name lookup
- nslookup
- unix
title: Managing DNS locally with /etc/hosts
url: /2013/10/29/managing-dns-locally-with-etchosts

---

Before the advent of a distributed domain name system; networked computers used local files to map hostnames to IP addresses. On Unix systems this file was named `/etc/hosts` or "the hosts file". In those days, networks were small and managing a file with a handful of hosts was easy. However as the networks grew so did the methods of mapping hostnames and IP addresses.

In modern days with the internet totaling at somewhere around 246 million domain names (as of 2012) the hosts file has been replaced with a more scalable distributed DNS service. While the hosts file is not used to map all hostnames to IP's these days it can still be quite useful if used properly and it can also be a source of trouble if not understood or used properly.

## Times to use the /etc/hosts

### A Local Network for Desktop Environments

Using the /etc/hosts file to give a human readable name to a local system within a desktop environment is perfectly reasonable. The hosts file is great to use in a home network or even in a small business environment where the machine count is only a handful of systems. As a side note the hosts file can be used to provide DNS for a local system but it can also be used to [restrict access](http://someonewhocares.org/hosts/hosts) to domains as well.

The best part of this is that the majority of Desktop Operating Systems have some sort of hosts file and they all follow roughly the same syntax, including Windows & OSX.

### Critical services in a enterprise server environment

Let's face it, sometimes local DNS systems can break. If you have servers that connect to critical systems via hostnames it may be wise to add the IP and hostname into the hosts file. This allows you to keep the connectivity to these services alive even during a local DNS outage.

**A word of warning** however, this extra security comes with a price. While it is easy to mistype an IP address into a DNS system it is just as easy to mistype that IP address into a hosts file. By managing these IP's in hosts files it also adds the complexity of managing the hosts files and ensuring that they are 100% correct all of the time.

This method also only works if that critical system is always going to have the same IP address, if DNS load balancing is used to reroute traffic for this critical system than it is not advisable to add this to the hosts file as it would circumvent the DNS failover.

### Specific Application Environments

Not every application environment has hundreds of servers that fill the same role, in enterprise environments it is quite common to see a smaller set of servers that are used for a specific application. That application may have a dedicated database server and/or dedicated web servers. In environments like this it is not uncommon to add each host in the environment into the hosts file. The same warnings apply in this environment as the one above, sometimes having hostnames go to DNS is the preferred method when the IP address of that system may change. However if the IP address is static and you do not trust your internal DNS system to be accurate or available, adding the IP into `/etc/hosts` is worth the effort.

As a note, when you choose to use the hosts file you also take the responsibility of having to manage this file and manage the accuracy of the file. This is easier with configuration management tools but even this can become troublesome if the IP's of hosts change and the configuration is not kept up to date.

## Times not to use the /etc/hosts file

### Server environments at scale

Whenever managing a large set of servers thousands upon hundreds of thousands of systems. Using the `/etc/hosts` file to map systems can be quite difficult and should only be used to map to systems that are serviced from static IP addresses. In large scale environments however, a service is usually provided by multiple IP addresses and that load balancing is driven by an internal DNS system.

## Adding a domain to /etc/hosts

Below I am going to show how to use the `/etc/hosts` file to locally point a domain to another IP. This can be used as a general example of how to add a domain or short hostname into the hosts file.

### Our example domain

In our example we are going to use example.com which today resolves to 93.184.216.119.

    $ ping -c 1 example.com
     PING example.com (93.184.216.119) 56(84) bytes of data.

### Adding the host name & domain name to the /etc/hosts file

To add our example we will first need to open the hosts file with vi or your favorite editor.

    $ sudo vi /etc/hosts

**Append:**

    # IP Domain ShortHost
    192.168.0.193 example.com example

### Ensure nsswitch.conf is correct

Before we go off checking if the resolution is correct let's ensure that the nsswitch.conf file is correct. The nsswitch.conf file controls in which order services will be consulted for name service lookups, in our case we are looking for the **"hosts"** service.

    $ grep host /etc/nsswitch.conf
     hosts: files dns

This setting is based on order, if files is before dns than the system will consult the `/etc/hosts` file before checking DNS for name service requests. However, if DNS was before files than the domain lookup would always go to DNS first.

### Validating the new resolution

As you can see from the ping command example.com now resolves to 192.168.0.193 and not 93.184.216.119.

    $ ping -c 1 example.com
    PING example.com (192.168.0.193) 56(84) bytes of data.

#### Don't use host or nslookup commands

Using the host or nslookup command to validate the change will not work and will simply cause confusion. Both of these commands will consult DNS and ignore the settings in `hosts` and `nsswitch.conf`.

    $ host example.com
     example.com has address 93.184.216.119

The fact that the host and nslookup command commands do not return the same result as the hosts file entry adds to the complication of using `/etc/hosts`. 3 months down the line when you are troubleshooting connectivity to example.com and the host command returns a valid result it will be easy to forget that you added it to the hosts file. My advice is, if you are going to use the hosts file make sure that the reason you are using it is valid and that it is the only way to accomplish what you need.

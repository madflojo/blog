---
authors:
- Benjamin Cane
categories:
- Linux
- Redis
- stunnel
- Security
date: '2014-02-18T08:50:00'
description: This article covers how to secure and encrypt redis traffic by using
  stunnel. Redis does not by default support SSL encryption, by using stunnel you
  can forward all redis traffic through a specified SSL tunnel.
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- redhat
- centos
- stunnel
- ssl wrapping
- ssl tunnel
- security
- encrypt redis traffic
- openssl
- self signed certificate
- redis ssl
- redis
title: Sending redis traffic through an SSL tunnel with stunnel
url: /2014/02/18/sending-redis-traffic-through-an-ssl-tunnel-with-stunnel

---

Lately if you have been paying attention to tech or even mainstream media you might have seen a few stories about data breaches. Sometimes these data breaches have allowed attackers to gather unencrypted passwords or credit card numbers. In the past these types of attacks still happened, but there was not as many attacks as today and when they happened they were kept secret. With more and more internet based services becoming part of peoples lives, there is even more targets for attackers who are looking to get sensitive data.

These attackers can often be quite crafty on the ways they get this data, many times they do it by gaining access to a database but another common place to capture and steal data is through unencrypted network traffic. There are many commonly used services that either do not support SSL encryption or that option is rarely used. Redis a distributed memory cache is a newer service that at this time does not support SSL connections. I've been using Redis lately on one of my side projects, but I keep finding myself limited by the lack of SSL encryption.

## Redis Security

Redis has been designed for use within a trusted private network, and does not support SSL encrypted connections. While that is ok for many implementations, it does not lend well to cloud based implementations. While some cloud providers offer private networks, not all of them do. So if you want to run a Redis master on one server and your application on another, you have no choice but to leave that connection unencrypted. Leaving that sensitive traffic to be sent across the cloud providers network or even the general internet with no protection from someone with a network sniffer. 

In this article I am going to show you how to secure your redis connections with stunnel, this article should handle the SSL part of securing a connection but you should also follow the other recommendations in [Redis Security](http://redis.io/topics/security).

## What is stunnel

The stunnel application is a SSL encryption wrapper that can tunnel unencrypted traffic (like redis) through a SSL encrypted tunnel to another server. While stunnel adds SSL encryption it does not guarantee 100% that the traffic will never be captured unencrypted. If an attacker was able to compromise either the server or client server they could capture unencrypted local traffic as it is being sent to stunnel.

## Wrapping redis traffic in SSL with stunnel

In today's article we will use stunnel to encrypt traffic from a **client** host to a **server** host. We will install stunnel on both the **client** and **server** hosts and establish a tunnel that redirects `localhost:6379` on **client** to the redis instance running on **server**. 

### Setting up the server host

We will first install redis and then setup stunnel to forward connections from external sources to the local redis instance.

#### Install the redis-server package

To install redis we will use `apt-get`.

    root@server:~# apt-get install redis-server

#### Configure the redis-service

After installation we only need to make one change to the redis configuration. For better security we will enable `requirepass` which requires all clients to authenticate before being able to pull or put data from the redis instance.

    root@server:~# vi /etc/redis/redis.conf

**Find:**

    # requirepass foobared

**Replace With:**

    requirepass <yourpass>

**Example:**

    requirepass foobared

#### Restart the redis service

Upon installation `redis-server` is started automatically, in order for our configuration changes to take effect we will need to restart the instance.

    root@server:~# /etc/init.d/redis-server restart

#### Install stunnel

Now that redis is installed and running we will install stunnel. For ease we will install stunnel with `apt-get` as well.

    root@server:~# apt-get install stunnel4

#### Start stunnel on boot

Unlike redis, stunnel doesn't start on boot automatically. To start stunnel on boot we will need to edit the `/etc/default/stunnel` file.

    root@server:~# vi /etc/default/stunnel4 

**Find:**

    ENABLED=0

**Replace With:**

    ENABLED=1

#### Creating a self signed certificate

Like any other SSL protocol stunnel requires a certificate to use for client to server communication. While you could get a signed certificate from a certificate authority such as Verisign, since we are using this for internal purposes only we can create a self signed certificate.

##### Generating a key

First we will create a private key, I am using `openssl` to create a 4096 bit RSA key. In my example I am using 4096 bit key as it [adds more security](http://danielpocock.com/rsa-key-sizes-2048-or-4096-bits) than a 1024 or 2048 bit key.

    root@server:~# openssl genrsa -out /etc/stunnel/key.pem 4096

##### Creating the certificate

Now that we generated a key we will now create a certificate. When generating the certificate we will be asked a series of questions; the answers provided are used to prove the validity of the certificate. The `-days` flag specifies the number of days this certificate is valid for, you can modify this if you need to but 5 years should be good enough.

    root@server:~# openssl req -new -x509 -key /etc/stunnel/key.pem -out /etc/stunnel/cert.pem -days 1826

Since this is really only being used for internal communications there isn't a right or wrong answer to these, but the below example can be used as a guide for answering the certificates question.

**Example:**

    root@server:~# openssl req -new -x509 -key /etc/stunnel/key.pem -out /etc/stunnel/cert.pem -days 1826
    You are about to be asked to enter information that will be incorporated
    into your certificate request.
    What you are about to enter is what is called a Distinguished Name or a DN.
    There are quite a few fields but you can leave some blank
    For some fields there will be a default value,
    If you enter '.', the field will be left blank.
    -----
    Country Name (2 letter code) [AU]:US
    State or Province Name (full name) [Some-State]:Arizona
    Locality Name (eg, city) []:Phoenix
    Organization Name (eg, company) [Internet Widgits Pty Ltd]:BenCane.com
    Organizational Unit Name (eg, section) []:
    Common Name (e.g. server FQDN or YOUR name) []:bencane.com
    Email Address []:testing@example.com

##### Combining the two files

We will combine both the key and certificate into a single file for stunnel to use. We will also change the file permissions to restrict who has access to read these key files.

    root@server:~# cat /etc/stunnel/key.pem /etc/stunnel/cert.pem > /etc/stunnel/private.pem
    root@server:~# chmod 640 /etc/stunnel/key.pem /etc/stunnel/cert.pem /etc/stunnel/private.pem

#### Configuring stunnel

By default stunnel reads all `*.conf` files in `/etc/stunnel/`. We will create a file named `redis-server.conf` and place our configuration within it.

    root@server:~# vi /etc/stunnel/redis-server.conf

**Add:**

    cert = /etc/stunnel/private.pem
    pid = /var/run/stunnel.pid
    [redis]
    accept = <yourexternalip>:6379
    connect = 127.0.0.1:6379
    
**Example:**

    cert = /etc/stunnel/private.pem
    pid = /var/run/stunnel.pid
    [redis]
    accept = 10.0.3.65:6379
    connect = 127.0.0.1:6379
    
By default redis listens to the `localhost` IP `127.0.0.1` on port `6379`. Our configuration has stunnel `accept` connections on the external IP and forward the connections to the redis instance listening on `127.0.0.1:6379`.

#### Starting stunnel

After the configuration file is in place we will start stunnel.

    root@server:/etc/stunnel# /etc/init.d/stunnel4 start

### Setting up the client host

At this point the **server** host is setup and ready, and we need to setup the **client** server to initiate the SSL tunnel with stunnel.

#### Installing redis-server

For this example we will install `redis-server` on the **client** as well; though this step is only to install the `redis-cli` tool. Most likely you would not need to install `redis-server` if you are using this setup for an application running on the **client** host; so keep in mind this part is optional.

    root@client:~# apt-get install redis-server

##### Do not start redis-server on boot

By default redis starts on boot, however we do not want redis to be running on the **client** host. To disable redis from starting on boot we can use the `update-rc.d` command.

    root@client:~# /etc/init.d/redis-server stop
    root@client:~# update-rc.d redis-server disable

#### Install stunnel

Installing stunnel on the **client** is similar to the **server** installation, minus some configuration differences.

    root@client:~# apt-get install stunnel4

#### Start stunnel on boot

To have stunnel start on boot we will need to edit the `/etc/default/stunnel4` file.
    
    root@client:~# vi /etc/default/stunnel4

**Find:**
    
    ENABLED=0
    
**Replace With:**

    ENABLED=1

#### Copy the certificate file from server to client

In order to establish an SSL connection we will need the `private.pem` file that we generated on the **server** host. You should always practice good certificate management with this key, if it was to fall into the wrong hands then the attacker could decrypt any SSL traffic that was previously captured
    
    root@client:~# scp root@10.0.3.65:/etc/stunnel/private.pem /etc/stunnel/
    root@client:~# chmod 640 /etc/stunnel/private.pem

#### Configure the stunnel client

The stunnel client configuration is very similar to the server configuration, to specify this stunnel instance is a client we will add `client = yes` to the configuration.
    
    root@client:~# vi /etc/stunnel/redis-client.conf

**Add:**
    
    cert = /etc/stunnel/private.pem
    client = yes
    pid = /var/run/stunnel.pid
    [redis]
    accept = 127.0.0.1:6379
    connect = <serverip>:6379

**Example:**

    cert = /etc/stunnel/private.pem
    client = yes
    pid = /var/run/stunnel.pid
    [redis]
    accept = 127.0.0.1:6379
    connect = 10.0.3.65:6379

On a client instance the `accept` and `connect` settings are reversed from the server configuration. This tells stunnel to listen locally on port `6379` and forward connections to the **server** host IP with port `6379`.

#### Start stunnel

Once the configuration is in place we can start the stunnel service.
    
    root@client:~# /etc/init.d/stunnel4 start

### Testing the connections

Now that both the **server** and **client** hosts have stunnel installed and a SSL tunnel established we can test this connection by using the `redis-cli` command to connect to localhost on the **client**.
    
    root@client:~# redis-cli -h localhost 
    redis localhost:6379> auth foobared
    OK

The way this configuration works is when a client on the **client** host connects to port `6379` locally it will be forwarded through the SSL tunnel that stunnel has created with the **server** host and redirected to the redis instance running on **server**. To setup an application to call this instance you would simply install the application on the **client** host and have it connect to redis on localhost the same way my example showed.

This same setup could also be used for setting up Master/Slave replication in redis, however the Slave instance would need to listen to a port other than the default `6379`. 

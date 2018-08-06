---
authors:
- Benjamin Cane
categories:
- Applications
- Databases
- How To and Tutorials
- Redis
date: '2013-11-12T08:00:52'
description: A guide on how to install Redis and setup Master - Slave replication
  between two or more Redis instances
draft: false
header:
  caption: ''
  image: ''
tags:
- high availability
- redis
- replication
- linux
- nosql databases
- nosql
- in memory cache
- memcache
- redis replication
title: Installing Redis and setting up Master - Slave Replication
url: /2013/11/12/installing-redis-and-setting-up-master-slave-replication

---

Over the past few years the usage of NOSQL databases has grown quite a bit. Part of this popularity is due to the scalability and performance seen with NOSQL solutions, one of those highly performant databases is Redis. Redis is an highly popular open source in memory key - value data store that is currently in use at and highly praised by tech companies such as Twitter, Stack Exchange and Github.

I've been following Redis for quite some time now and finally had a project that had a good use case for it. The setup of Redis was so easy that I thought it would be a good idea to share how to install and configure a Redis instance for Master - Slave replication.

## What is Master - Slave Replication?

Master - Slave replication is a data replication concept seen often in the database world. This replication allows for a database service to replicate data written to the master instance to a slave instance. This slave instance could be located within the same facility for scaling out read requests or in another facility in order to mitigate a disaster recovery scenario.

In general slave servers are read only, Redis is no different; however it does have the ability to override this setting however data only written to the slave will be lost during a resynchronization to the master server. Usually a Master server can have many slave servers setup, in the case of Redis a slave server can also serve as the master server for other slaves. This configuration allows one to send all write requests to the single master server and be able to scale out any read requests against many slaves.

## Setup the Master Server

### Install the Server

In this article we will be installing Redis on Ubuntu 13.10; we can do this using the apt package manager.

    ubuntu@redis-master:~$ sudo apt-get install redis-server

### Configuration

Before starting Redis we will need to configure a few items within the `/etc/redis/redis.conf` configuration file.

    ubuntu@redis-master:~$ sudo vi /etc/redis/redis.conf

#### Changing the Listening Interface

By default Redis binds to the localhost IP, this would be fine if we were only using Redis locally. In this example however we are setting up replication and will need to change the bind address to the public IP.

**Find:**

    bind 127.0.0.1

**Replace with:**

    bind <youripaddress>

**Example:**

    bind 10.0.3.61

#### Adding Password Authentication

Redis does not have a concept of users and permissions that you would see with a traditional database such as MySQL, however Redis does have a simple password based authentication. To require password based authentication we will need to un-comment the `requirepass` setting.

**Find:**

    # requirepass foobared

**Replace with:**

    requirepass somesuperlongpasswordthathaslotsofspecialcharacters

### Restart the Redis Server

At this point after saving the configuration file we will restart the redis-server service.

    ubuntu@redis-master:~$ sudo /etc/init.d/redis-server restart

## Installation on the Slaves

Setting up a Redis Slave is the same as setting up the master; however we will need to add a few more configuration steps.

### Install the Redis Server package

    ubuntu@redis-slave:~$ sudo apt-get install redis-server

### Configuration

We will again need to modify the Redis server configuration file.

    ubuntu@redis-slave:~$ sudo vi /etc/redis/redis.conf

#### Changing the Listening Interface

Again we will change the bind address to the public IP address of the slave server.

**Find:**

    bind 127.0.0.1

**Replace with:**

    bind <youripaddress>

#### Adding Password Authentication

While slave systems are read only by default it is a good idea to enable password authentication to prevent clients from reading data without authenticating. This setting is optional, if you do not care about securing the data being read than this can stay commented.

**Find:**

    # requirepass foobared

**Replace with:**

    requirepass somesuperlongpasswordthathaslotsofspecialcharacters

#### Setting up Replication

The below steps will outline setting up replication from the Slave. Replication only needs to be defined on Slave systems, the Master server does not require any special configuration.

##### Specifying the Master

In the slave configuration file specify the master server to replicate from. Redis has the ability to replicate from a slave, to set this up you would simply specify the first slaves details in place of the master.

**Find:**

    # slaveof <masterip> <masterport>

**Replace With:**

    slaveof <masterip> <masterport>

**Example:**

    slaveof 10.0.3.61 6379

##### Authentication

If you set a password earlier for the master server you will need to specify that password via the `masterauth` setting.

**Find:**

    # masterauth <master-password>

**Replace With:**

    masterauth somesuperlongpasswordthathaslotsofspecialcharacters

### Start the Service

At this point we can start the redis-server on the slave.

    ubuntu@redis-slave:~$ service redis-server start

## Testing Replication

To test the replication we will first login to the master server and set a key-value.

### Set the key-value on the Redis Master

To login to the Redis server we will use the redis-cli client. The -h flag specifies the host to connect to, by default the `redis-cli` will connect to the localhost IP.

    ubuntu@redis-master:~$ redis-cli -h 10.0.3.61

Once logged in use the `AUTH` command with the password specified earlier.

     redis 10.0.3.61:6379> AUTH <password>
     OK

After authenticating we can now set a key-value pair using the `SET` command.

     redis 10.0.3.61:6379> SET replicated:test true
     OK

### Get the key-value on the Redis Slave

Now that data has been saved to the master we will login to the Redis Slave server using the same redis-cli command and use the `GET` command to retrieve the replicated data.

    ubuntu@redis-slave:~$ redis-cli -h 10.0.3.251
    redis 10.0.3.251:6379> AUTH foobared
    OK

Once logged in use the `GET` command to retrieve the value from the `replicated:test` key

     redis 10.0.3.251:6379> GET replicated:test
     "true"

At this point we have installed Redis on two systems and setup replication between them. If you required a third server you could repeat the Slave setup steps and either use the Master or Slave server as the source server.

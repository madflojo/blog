---
author: madflojo
date: 2014-12-23 07:50:00-07:00
pubdate: Tue, 23 Dec 2014 07:50:00 -07:00
popularity: False
slug: building-self-healing-applications-with-salt-api
title: "Building Self-Healing Applications with Saltstack"
description: This article will explore creating an application that detects errors and corrects them by utilizing Saltstacks API
post_id: 125
categories:
- Python
- Saltstack
tags:
- saltstack
- self healing applications
- salt-api
- python
- devops
- automation
---

Self healing infrastructure and applications is always something that has piqued my interested. The first iteration of self healing infrastructure that I came across was the Solaris Service Management Facility aka "SMF". SMF would restart services if they crashed due to hardware errors or general errors outside of the service itself. Today there are quite a few more ways of implementing self healing and we are going to explore a different way of going about it. 

In today's article we are going to build a method for an application to initiate automated actions to repair database issues.

## Why detect issues from the application layer

Traditional self healing has always been external to the application but with today's environments it is possible to integrate automation tools like Saltstack with the applications error handling. What better place to detect issues with an application than the applications code itself?

Before we start lets better understand what application we are modifying. 

## Overview

Lately I have been working quite a bit on one of my projects [Runbook](https://runbook.io). Runbook utilizes [RethinkDB](http://rethinkdb.com/) for it's database and while RethinkDB is great as it is today it lacks automatic failover. This means if one of the database servers in the cluster is down any data that server was the master of is not available. At least not until someone either brings up the database instance or declares it dead on another member of the cluster.

The application we are going to make self healing is a component within Runbook. This component is the **actioner** process, which [as it is today](https://github.com/asm-products/cloudroutes-service/blob/ef6211a6fa05bf8a00f0c73c998c686bb0fb0904/src/actions/actioner.py) is already able to continue processing even with RethinkDB is down. It does this by first reading from Redis and then reading from RethinkDB, if RethinkDB is down than the process will use the information it obtained from Redis.

You can see this in action with the following python code.

```
def getMonitor(cid):
    ''' Lookup a monitor via either rethinkdb or redis '''
    # Pull from redis first
    cache = lookupRedis("monitor", cid)

    # Pull from RethinkDB second
    try:
        results = r.table('monitors').get(cid).run(rdb_server)
        results['cacheonly'] = False
        if int(cache['failcount']) > results['failcount']:
            results['failcount'] = int(cache['failcount'])
    except (RqlDriverError, RqlRuntimeError, socket.error) as e:
        results = cache
        results['cacheonly'] = True
        logger.critical("RethinkDB is unaccessible, monitor %s was pulled from cache" % cid)
        logger.critical("RethinkDB Error: %s" % e.message)
    return results
```

When the above code experiences an error pulling data from RethinkDB it not only sets the data returned from Redis as the results it also adds a key called `cacheonly` and sets it's value to `True`. This value is used later in the application after it has completed processing to tell it to attempt to reconnect to RethinkDB.

```
        if cacheonly is True:
            logger.critical("Process is in cacheonly mode: attempting reconnect")
            try:
                rdb_server.reconnect()
                logger.info("Connected to Rethinkdb on port %s" % config['rethink_port'])
                cacheonly = False
            except (RqlDriverError, RqlRuntimeError) as e:
                logger.critical("RethinkDB Error: %s" % e.message)
            except:
                logger.critical("Got non-RethinkDB Error... I should be restarted when RethinkDB is up")
```

The above code checks if `cacheonly` is `True` and if it is it attempts to reconnect to RethinkDB. For many this in itself can be considered self healing, as the application detects an issue with the database and attempts a reconnection to resolve the issue. We can do more however; much more.

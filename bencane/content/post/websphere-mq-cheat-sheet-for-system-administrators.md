---
authors:
- Benjamin Cane
categories:
- All Articles
- Applications
- Cheat Sheets
- Linux
- Linux Commands
- Middleware
- WebSphere MQ
date: '2013-04-22T23:50:22'
description: A simple cheat sheet that shows commands every sysadmin managing WebSphere
  MQ could use
draft: false
header:
  caption: ''
  image: ''
tags:
- ibm
- linkedin
- linux
- listener
- mq
- queue manager
- scripts
- system administrators
- websphere mq
- websphere mq cheat sheet
title: Websphere MQ Cheat Sheet for System Administrators
url: /2013/04/22/websphere-mq-cheat-sheet-for-system-administrators

---

IBM's Websphere MQ is a middle-ware application that allows two applications to pass messages back and forth without having to integrate with each-other directly. Websphere MQ is a fairly popular application in the enterprise especially for those running many java based programs.

Today's article is a copy of my personal Websphere MQ cheat sheet. This cheat sheet is geared more from a System Administrators prospective and doesn't touch much on creating or altering queues or channels, but should provide a good head start for those who need to just get something restarted.

This cheat sheet is split into two parts, the first being the Linux command line based commands and the second being the MQ CLI based commands.

_Where the command starts with REPLACE will require replacing the information with information from your system_

## Linux Command Line Commands

The majority of these commands are run as the mqm (or equivalent) user. By default these commands are in `/opt/mqm/bin` which I would advise adding to the mqm users PATH.

#### Create a Queue Manager

    $ crtmqm REPLACE_QMGR_NAME

#### Delete a Queue Manager

    $ dltmqm REPLACE_QMGR_NAME

#### Start Queue Manager

    $ strmqm REPLACE_QMGR_NAME

#### Stopping Queue Manager

##### Wait for queue manager to shutdown

    $ endmqm -w REPLACE_QMGR_NAME

##### End Immediately

    $ endmqm -i REPLACE_QMGR_NAME

#### Start Queue Manager (Init Script)

By default Websphere MQ does not ship with an init script, you can add this functionality via a [support pac (MSL1)](http://www-01.ibm.com/support/docview.wss?uid=swg24016554) provided by IBM.

    $ service ibm.com-WebSphere_MQ start

#### Stopping Queue Manager (Init Script)

    $ service ibm.com-WebSphere_MQ stop

#### Start MQ Listener

    $ echo "start LISTENER(SYSTEM.DEFAULT.LISTENER.TCP)" | runmqsc REPLACE_QMGR_NAME

#### Stop MQ Listener

    $ echo "stop LISTENER(SYSTEM.DEFAULT.LISTENER.TCP)" | runmqsc REPLACE_QMGR_NAME

#### Display Queue Managers & Status

    $ dspmq

#### Set MQ Privileges

In order for a Unix user to start utilizing MQ they must have the appropriate privileges. You can find the available privileges in [IBM's Documentation](http://publib.boulder.ibm.com/infocenter/wmqv6/v6r0/index.jsp?topic=%2Fcom.ibm.mq.amqzag.doc%2Ffa15980_.htm).

##### Set MQ Privileges By User

    $ setmqaut -m REPLACE_QMGR_NAME -t qmgr -p REPLACE_USER REPLACE_PLUS_OR_MINUS_PRIVILEGE

##### Set MQ Privileges By Groups

    $ setmqaut -m REPLACE_QMGR_NAME -t qmgr -g REPLACE_GROUP REPLACE_PLUS_OR_MINUS_PRIVILEGE

#### Display MQ Privileges

##### Display MQ Privileges By Users

    $ dspmqaut -m REPLACE_QMGR_NAME -t qmgr -p REPLACE_USER

##### Display MQ Privileges By Groups

    $ dspmqaut -m REPLACE_QMGR_NAME -t qmgr -g REPLACE_GROUP

#### Lookup MQ Error Numbers

    $ mqrc REPLACE_ERROR_NUM

#### MQ Sample Scripts

Within the MQ release by IBM there is a package that contains sample scripts for MQ. There are about 3 of these sample scripts that I have found pretty useful.

##### Pop (GET) Messages off a queue

    $ amqsget REPLACE_Q_NAME REPLACE_QMGR_NAME

This command will remove messages from the queue, only use this if you no longer want the messages in the queue.

##### Browse Messages in a queue

    $ amqsbcg REPLACE_Q_NAME REPLACE_QMGR_NAME

##### Open a Queue for writing

    $ amqsput REPLACE_Q_NAME REPLACE_QMGR_NAME

When you find yourself with a system that is connected to a repository but doesn't see new messages you can try opening the queue for writing with amqsput to "refresh" the connectivity. You do not have to write anything to the queue. Simply open the queue and press `ctrl+d` without typing any additional characters.

#### Open Websphere MQ CLI

    $ runmqsc REPLACE_QMGR_NAME

## Websphere MQ CLI Commands

The following commands are to be run directly from the MQ command line interface.

#### Start MQ Listener

    start LISTENER(SYSTEM.DEFAULT.LISTENER.TCP)

#### Stop MQ Listener

    stop LISTENER(SYSTEM.DEFAULT.LISTENER.TCP)

#### Disable Channel Authentication

    alter qmgr chlauth(disabled)

Channel Authentication is new as of MQ 7.0. If your systems don't use it you can simply turn it off.

#### Display Queues

##### All Queues

    display queue(*)

##### Specific Queues

    display queue(REPLACE_Q_NAME)

##### Short hand

    dis q(REPLACE_Q_NAME)

#### Display Local Queues only

##### All Queues

    display qlocal(*)

##### Specific Queue

    display qlocal(REPLACE_Q_NAME)

##### Short hand

    dis ql(REPLACE_Q_NAME)

#### Display Alias Queues only

##### All Queues

    display qalias(*)

##### Specific Queue

    display qalias(REPLACE_Q_NAME)

##### Short hand

    dis qa(REPLACE_Q_NAME)

#### Display Cluster Queues only

##### All Queues

    display qcluster(*)

##### Specific Queue

    display qcluster(REPLACE_Q_NAME)

##### Short hand

    dis qc(REPLACE_Q_NAME)

#### Display Channels

##### All Channels

    display channel(*)

##### Specific Channel

    display channel(REPLACE_CHANNEL_NAME)

##### Short hand

    dis channel(REPLACE_CHANNEL_NAME)

#### Display Channel Status

##### All Channels

    display chstatus(*)

##### Specific Channel

    display chstatus(REPLACE_CHANNEL_NAME)

##### Short hand

    dis chstatus(REPLACE_CHANNEL_NAME)

#### Display Local Queue Manager Information

    display qmgr

#### Display Cluster Queue Manager Information

    display clusqmgr(REPLACE_CLUSQMGR_NAME)

#### Show number of INPUT and OUTPUT threads open

    display qstatus(REPLACE_Q_NAME) IPPROCS OPPROCS

#### Find Process ID of Processes Accessing Queue

    display qstatus(REPLACE_Q_NAME) TYPE(HANDLE) ALL

#### Refresh Cluster Queue Manager

    refresh cluster(REPLACE_CLUSQMGR_NAME)

#### Start Channel

    start channel(REPLACE_CHANNEL_NAME)

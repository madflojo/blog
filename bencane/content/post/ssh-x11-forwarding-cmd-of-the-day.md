---
authors:
- Benjamin Cane
categories:
- Command Line
- Linux
- Linux Commands
- Unix
- Unix Commands
date: '2011-08-09T20:30:05'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- ssh
- tech
- x11
title: 'ssh: X11 Forwarding'
url: /2011/08/09/ssh-x11-forwarding-cmd-of-the-day

---

One of the coolest uses of ssh I've had to use recently is the X11 forwarding. In my case I had a java application that opened up a GUI but I had to run it from a server that did not have a running graphical user environment as it was in init state 3.

The answer is far simpler than one would initially think. With the ssh client you are able to connect to a server and enable X11 forwarding. For me this meant I could connect to my server in init(3) via my local machine enabling X11 and launch the GUI.

To try it out yourself simply run

    $ ssh -X user@remotehost

Once you login kick off a GUI tool like firefox.

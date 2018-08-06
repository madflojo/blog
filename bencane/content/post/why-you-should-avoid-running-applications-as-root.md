---
authors:
- Benjamin Cane
categories:
- Administration
- All Articles
- Best Practices
- Linux
- Security
- Unix
date: '2012-02-20T15:24:29'
draft: false
header:
  caption: ''
  image: ''
tags:
- apache
- bsd
- debian
- linux
- nginx
- security
- sudo
- suid
- tech
- unix
title: Why you should avoid running applications as root
url: /2012/02/20/why-you-should-avoid-running-applications-as-root

---

I'm going to start this post by saying what I'm really thinking. 90% of the time if an application is running as the root user on a Unix/Linux machine; it is because the sysadmin who setup or designed the environment was being lazy.

Now before getting offended, being a lazy sysadmin is a good thing. The fact is that most systems administrators are lazy in some way, and that is the reason why most systems administration tasks end up being scripted. In the systems administration world, laziness breeds efficiency.

With that said there is one thing that a sysadmin must never take the lazy way out of, **Security**. One of the basic concepts of security is restricting users to only the privileges that they require. The same can be and should be applied to applications running on your system, only provide the privileges that your application requires.

One easy way to do this is to avoid running applications as root whenever possible. When an application is running as the root user that application has the ability to control your server. If an attacker gains control of that application then they can perform any task they want on your server, if you are running SELinux there is an additional security control; but even then an application that runs as root can potentially disable all of your additional security controls.

**Real World Example:**

Let's say that **Mr. Sys Admin** decided to take the lazy way out and run his apache web server as root. On his web server he hosts his friend **Bob's** Photo Gallery; **Bob's** photo gallery software has a bug that allows users to upload a file that is named .JPG but does not check if the file is actually an Image file. **Attacker A** knows of this bug and decides to upload a malicious script that adds a second user with the same uid as root. **Attacker A** uploads this file and executes it by calling a webpage.

Because **Mr. Sys Admin** decided to run his web server as root the attackers script ran as root and was able to add the user to the system. **Attacker A** now has full root access to **Mr. Sys Admin's** server.

I used Apache as an example but this same type of scenerio can apply to any application.

There are always reasons someone can justify wanting to run an application as root; lower port assignment, modifying files from other applications, executing system tasks, etc. But at the end of the day these reasons can usually be worked around using things like Sudo, SUID, SGID, sticky bit, iptables, and a good user/group configuration.

A good user & application privileges policy can save you, your company, and your users a lot of time and money by providing an additional layer of security.

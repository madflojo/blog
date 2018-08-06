---
authors:
- Benjamin Cane
categories:
- Administration
- All Articles
- Linux
- Unix
date: '2012-04-01T19:28:31'
draft: false
header:
  caption: ''
  image: ''
tags:
- fedora
- linkedin
- linux
- oracle
- PuTTY
- ssh
- tech
- ubuntu
- unix
- vdi
- virtualbox
- windows
- Windows Tools
title: 'Sysadmin Tools: Managing Linux from a Windows Desktop'
url: /2012/04/01/sysadmin-tools-managing-linux-from-a-windows-desktop

---

While it is getting more common for companies to allow their IT staff to choose their own OS not every company allows this. In fact most companies require their IT staff to use Windows, as Windows has historically been the dominate OS for the business world. While I personally believe it is easier to administer Linux/Unix servers using a Linux desktop this doesn't mean that I get to be the exception to the rule; sometimes I have had to use a Windows desktop.

Below is an outline of some various tools that I've used to help manage Linux/Unix servers in a Windows world.

## PuTTY Suite

#### PuTTY | [Download Here](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html)

PuTTY is the most popular SSH client for Windows. Everyone and anyone who has SSHed into a server from a Windows desktop has used PuTTY, and for good reason. It just works.

I find PuTTY is easy to understand for even the most novice user, feature rich (2 words SSH Tunnels), and open source (Windows & Unix). I think PuTTY is a great tool and I'm not alone as it has made the top 50 list on [Life Hackers: 50 Free Apps We're Most Thankful For](http://lifehacker.com/5698593/50-free-apps-were-most-thankful-for).

#### Pagent | [Download Here](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html)

While PuTTY is great there are some other tools that help it along as well. Pagent is a SSH key authentication agent, Pagent will allow you to import your RSA or DSA keys and works in conjunction with PuTTY to provide you with key based authentication.

All you have to do is import your private key into Pagent and push your public key to the server/servers you want to login to.

#### PuTTYgen | [Download Here](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html)

PuTTYgen works great with Pagent, it allows you to generate an RSA or DSA public/private key pair. You can use this with Pagent or use it just to generate RSA/DSA keys for your servers. I do want to point out that you are not required to use PuTTYgen for Pagent, Pagent will allow you to import private keys that were generated other places including Linux/Unix servers.

## Other PuTTY tools

While the PuTTY tools above are distributed by the original developer of PuTTY there are some other tools out there developed by others that help utilize PuTTY even more.

#### PuTTY Session Manager | [Download Here](http://puttysm.sourceforge.net/#download)

PuTTY Session Manager is probably one of my favorites; PSM uses the sessions that are saved using PuTTY and allows you to organize them and display them in folder trees within PSM. This is a great tool if your organization is just getting started and you do not have a database of the servers you manage. The Import/Export features let you use PuTTY Session Manager as your "list of servers" when you only have a few in your inventory.

PSM can launch PuTTY, Filezilla or WinSCP client connections to the server you choose. It also works well with Pagent to use key based authentication.

#### ClusterSHiSH | [Download Here](http://www.siftsoft.com/clustershish.html)

Ever have the need to run the same command on multiple hosts but don't have a server to kick off an SSH for loop from? What about hundreds of hosts? ClusterSHiSH can help. With only a few key strokes ClusterSHiSH can attach to all or a select few PuTTY windows and run whatever command you want. In the hands of a seasoned Systems Administrator this can be a great tool, in the hands of a sloppy typer this can be a nuclear bomb to your server farm. Discretion is advised.

[PuTTY Command Sender](http://www.millardsoftware.com/puttycs) can perform the same tasks as ClusterSHiSH however; I personally prefer ClusterSHiSH as you can use a checkbox to select what PuTTY windows you want to run the command in and PuTTY Command Sender uses a REGEX like rule to selectively choose. I feel a checkbox is a lot faster than a REGEX.

PuTTY Command Sender does have a win with the ability to hide password input, whereas ClusterSHiSH will only display its input in plain-text.

#### PuTTYcyg | [Download Here](http://code.google.com/p/puttycyg/downloads/list)

PuTTYcyg is a patched version of PuTTY that gives you an extra option to login to a local Cygwin terminal, if you are using Cygwin this is a must have.

## Linux & Linux-like Environments

Sometimes you just need a local command line environment, here are a couple of tools that can help you get there.

#### Cygwin | [Download Here](http://www.cygwin.com/)

I've used Cygwin off and on for the past 4 - 5 years, sometimes I love how close to Linux it is and sometimes I hate that its not exactly the same. If you want a Linux like command line environment on your Windows OS than Cygwin is great and while it is close it is still not exactly Linux.

#### Oracle VirtualBox | [Download Here](https://www.virtualbox.org/)

When you need the real thing at your finger tips VirtualBox can save the day. VirtualBox is an open source virtualization platform that you can install in your Windows OS and allows you to create and run Linux/Unix/Other virtual machines. When you install VirtualBox Guest Utils you can make your VM full screen and allow copy-paste between your Windows OS and your Virtual Machine.

For the past few years I've been using VirtualBox with an Ubuntu or Fedora virtual machine as I love having the power of Linux at my finger tips. The only downfall of this solution is that your desktop machine needs to have enough memory/cpu power to run the virtual machine inside (not hard to find with today's hardware).

## File Transfer Applications

#### FileZilla | [Download Here](http://filezilla-project.org/)

FileZilla is a great application, it can transfer files using FTP, FTPS, or SFTP. Whenever I want to get a file off a server and I can't use scp from my Cygwin or Linux VM command line, I use FileZilla.

#### WinSCP | [Download Here](http://winscp.net/eng/download.php)

While I personally like FileZilla, I believe that WinSCP has its place. Many companies allow the installation of WinSCP but not FileZilla and sometimes the other way around. In this post I'm not trying to say which one is better, I've used them both and I personally default to FileZilla, but WinSCP is good too.

These are just a few tools I've found extremely helpful, but I am always on the look out for more. If you know of any that I did not mention feel free to post it in the comments section.

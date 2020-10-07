---
authors:
- Benjamin Cane
categories:
- How To and Tutorials
- Security
date: '2011-10-12T01:11:00'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- spyware
- ubuntu
- unix
- vdi
- virtualbox
- windows
title: 'VirtualBox: Mom please stop getting spyware (Cheap VDI)'
url: /2011/10/12/virtualbox-mom-please-stop-getting-spyware-cheap-vdi

---

While I normally am able to avoid the desktop support role there is one person out there who ~~guilts~~ err.. convinces me to help her out. My mom.

I'm not going to sit here and bash my moms computer skills, in all actuality she is pretty good with a computer. In the past she figured out how to add a printer and print something with Ubuntu by herself.

The problem is my mom is a Windows user and she is the typical user who receives questionable emails and goes to certain sites that promise you win things but only infect your OS with spyware.

The last time I had to clean up her computer I decided to dual boot it with Ubuntu in order to prevent her from getting spyware. That endeavor was thwarted by the hands of Quickbooks, Tax Programs and Facebook games.

The problem I have with fixing my mom's computer is that every time she needs it fixed either she has to bring it to my house or I have to go to hers. This usually ends up taking a good day or so and honestly while I like visiting my mom I don't like having to spend the time fixing her computer. This also could mean she is without a working computer for weeks if I am travelling.


So yet again (several years later) I find myself having to fix my moms computer, but this time I'm getting creative.

**The solution to my headache:**

My goal is to install a Linux OS and use VirtualBox to create a VM Guest with Windows Vista (it's what she has..).Since the Windows VM Guest is doomed to be infected with spyware I am going to keep a clean install in a VM Guest powered off and use it as a template. This also has to be setup so that it is easy for my mom to use.

**Getting Linux Ready**

I've decided to use Ubuntu for this exercise because its quick to install, easy, a good OS in general, and my mom has some familiarity with it, in case she ever has to use it she can.

I did a plain default install of Ubuntu, then installed VirtualBox with apt-get.

    # apt-get install virtualbox-ose virtualbox-guest-additions

**VM Setup**

I've decided to first create a template VM that I can clone. I am doing this because my mom seems to have a knack at getting spyware/virii/malware on her computer. I plan to use snapshots to create backups but if her Windows system ever gets hosed beyond the backups than I have a quick option of recreating the VM by cloning the template.

To create the template I must create a new virtual machine, the process is no different from any other VM creation. Rather than reinvent the wheel and guide you through installing Windows in a VirtualBox guest I am going to send you to a good tutorial I found [Creating a Windows XP guest in VirtualBox for Linux.](http://reformedmusings.wordpress.com/2008/12/12/creating-a-windows-xp-guest-in-virtualbox-for-linux/)

_I didn't use this tutorial I only skimmed it_

Once I had the OS loaded, Guest Additions installed, and connected her external hd to the guest I went ahead and installed some basic applications that I know my mom uses (i.e firefox, ad blockers, windows security). At this point the virtual machine is ready. I could give this to my mom and she can use it, but before that I am going to create a template from this virtual machine in case I ever need to completely re-OS or re-deploy her Windows Desktop.

**VM Cloning**

To utilize the VM as a template I will first power it off and use cloning to create a VM. My mom will then use the VM as her desktop leaving the original VM Guest powered off ready to be cloned again if need be.

VirtualBox doesn't have a fancy right click > clone like other (normally higher end) virtualization technologies. Or at least the version that ships with Ubuntu does not. To create a clone you can use the `VBoxManage clonevdi` command.

    # VBoxManage clonevdi Template.vdi WinVista.vdi

The above command will create a new copy of the .vdi file; a vdi file is the Virtual Disk Image file that contains all of the virtual machines configuration and disk storage. Essentially everything about this Virtual Machine is stored in the .vdi file.

After the clone is complete I added a new virtual machine which asks if you want to create a new disk or use an existing. I elected to use WinVista.vdi (the clone vdi). After answering some basic questions I started the new virtual machine and everything was setup just as it was on the template.

**Starting the VM on boot**

At this point I now have a Windows Desktop that my mom can use running in a VM but before I call this finished I want to have the Windows desktop to appear to my mom without any effort. To do this I added the command `VBoxManage startvm "Windows Vista"` as a new entry to **System Settings > Startup Applications**.

    # VBoxManage startvm "Windows Vista"

Now when my mom boots the computer up she will see an Ubuntu login screen, once she logs into that system she will get a full screen Windows Desktop. She will still see the VirtualMachine management bar but I don't mind my mom seeing that as she wont mess with settings she doesn't understand.

I'm sure there are other ways to make the full screen VM show up without my mom having to login to Ubuntu but I elected to take the easy/lazy way out. This also gives my mom the option of closing the VM and going into Ubuntu in the off chance she needs to do anything on the host OS.

**Tasks for later**

Before giving the computer back to my mom I also set **opennssh-server** to start on boot so that I can manage the VirtualBox setup remotely.

    # apt-get install openssh-server  
    # update-rc.d ssh defaults

I will also remotely setup backups using a script and VBoxManage to create and rotate periodic snapshots of my moms desktop; maybe that will be another post.

**The Benefits**

After my mom starts using the Windows Desktop I've setup for her with VirtualBox; I can now rest easy knowing that if my mom gets her system infected again I can do any of the following.

  * Restore from recent snapshot - 15 minutes
  * Restore from weekly snapshot - 15 minutes
  * Deploy fresh image by cloning the template - 30 minutes

And the best part of this; I can do all of these tasks from anywhere with an internet connection. Not to mention that with snapshots I can upgrade her version of windows and if any of her programs don't play nice I can revert it in a matter of minutes using snapshots from the comfort a local coffee shop.

---
authors:
- Benjamin Cane
categories:
- All Articles
- How To and Tutorials
- Linux
- Troubleshooting
date: '2012-08-20T12:25:41'
draft: false
header:
  caption: ''
  image: ''
tags:
- apt
- apt-get
- i/o
- iostat
- kernel
- linkedin
- linux
- linux os
- linux system
- lsof
- network
- performance issues
- process
- production server
- red hat os
- rpm
- sar
- scripts
- stat
- system statistics
- systemtap
- troubleshooting
- ubuntu
- yum
title: Advanced Linux System Statistics and Diagnostics with SystemTap
url: /2012/08/20/advanced-linux-system-statistics-and-diagnostics-with-systemtap

---

In one of the first posts of this blog I covered some basic SystemTap functionality from an email that I sent to members of my team, but I have always felt that I haven't given SystemTap as thorough of an article as this incredible tool deserves. Today I want to correct that.

For today's article I will show how to compile SystemTap scripts on one server while running the compiled module on a production server without installing debug-info or devel packages in production.

## What is SystemTap?

SystemTap provides a command line and scripting language interface to probe both kernel and user space level information. Using SystemTap one can pull information from a Linux system that far exceeds the current implementations of utilities like `top`, `netstat`, `ps`, `lsof` and `iostat`.

While SystemTap is still being developed it has some [sample scripts](http://sourceware.org/systemtap/SystemTap_Beginners_Guide/useful-systemtap-scripts.html) already available for the average user and is immediately useful for anyone with tricky performance issues or a need to look deeper into any problem.

## SystemTap Requirements

For SystemTap scripts/modules to work SystemTap needs to have information about the running kernel, this information is available in the kernel-debuginfo and kernel-devel packages. In most environments running kernel-debuginfo and kernel-devel in production is not an option.

For users like this the SystemTap scripts can be compiled on a non-production system that has the debuginfo and devel packages installed and run the precompiled module on the production system that does not have those kernel packages installed.

SystemTap also has a server and client ability that allows for a machine with the client installed to compile and run the SystemTap script based on devel/debuginfo packages installed on the SystemTap server. However I will not be covering that setup in this article and will be saving that for another article.

### Installing SystemTap on the non-production system

On the non-production system called "Workstation" we will be compiling SystemTap scripts and converting them to modules for the production system called "Production".

#### Required Packages
	
  * Kernel-Debuginfo
  * Kernel-Devel
  * Kernel-Debuginfo-common
  * Systemtap
  * Systemtap-runtime

Since this is our non-production system and we will be compiling the scripts into modules for our production system we will need to have the Kernel and SystemTap packages listed above.

#### Find the needed Kernel Version

Because SystemTap requires specific versions of the kernel packages we need to look up which version of the kernel our production server is running. A server that is being used to compile scripts can have a different version of the kernel running however it must have the proper Kernel Debuginfo/Devel versions installed.

We can find the current running version in production with the `uname` command.
     
     root@production:~# uname -r
     3.2.0-29-generic

#### Install the Packages with apt-get

I will be installing the packages on my Ubuntu system with `apt-get`. The same steps can be performed with `yum` or with `rpm` for Red Hat/CentOS/OEL Linux distributions.

For Ubuntu versions above 9.04 you will need to add a package repository as outlined on the [SystemTap Wiki](http://sourceware.org/systemtap/wiki/SystemtapOnUbuntu).

##### Debug and Devel Info Package
     
     root@workstation:~# apt-get install -y linux-image-3.2.0-29-generic-dbgsym

##### SystemTap Packages
     
     root@workstation:~# apt-get install systemtap systemtap-runtime

Now that all of the required packages are installed I can compile scripts into modules on my workstation server and run them on my production server.

### Installing SystemTap on the production server

#### Required Packages
	
  * Systemtap-runtime

##### Install the Packages with apt-get

Since we are running the SystemTap modules precompiled on the production server, we only require the `systemtap-runtime` package.
     
     root@production:~# apt-get install systemtap-runtime

## Compiling A SystemTap Script

For our example module we will use the SystemTap script nettop which provides network statistics in a top style fashion. We will first compile this on the workstation server and transfer it to the production server via scp or some other method.
     
     # stap -r Kernel_Version Script -m Module_Name

**Example:**
     
     root@workstation:~# stap -r 3.2.0-29-generic nettop.stp -m nettop_stap

After stap has finished compiling the module it will start running, to stop the module simply press `CTRL-C`.

## Running the Compiled SystemTap Module

Once the script is compiled it is now a SystemTap module and it can be copied to the production server and run with the staprun command.
     
     # staprun Module_Name

**Example:**
     
     root@production:~# staprun ./nettop_stap.ko
      PID UID DEV XMIT_PK RECV_PK XMIT_KB RECV_KB COMMAND
      1723 105 vnet0 3 0 0 0 qemu-system-x86
      1723 105 vnet1 3 0 0 0 qemu-system-x86
     
     PID UID DEV XMIT_PK RECV_PK XMIT_KB RECV_KB COMMAND
      1723 105 vnet0 2 0 0 0 qemu-system-x86
      1723 105 vnet1 2 0 0 0 qemu-system-x86
      2583 1000 eth0 1 0 0 0 sshd

### Detaching and Attaching the running SystemTap Module

If you wanted to keep the module running and be able to detach and attach it you can do this by starting it with the `-L` flag.

    # staprun -L Module_Name

**Example:**

    root@production:~# staprun -L nettop_stap.ko

    Disconnecting from systemtap module.
    To reconnect, type "staprun -A nettop_stap"

You can attach the process by running `staprun -A` and again detach the process by typing `CTRL-\`.

Using this setting you can attach to a running module at any time and it will show you recent data. This can be very useful if you are troubleshooting an issues and need to let the stap module run in the background while performing other commands.

### Monitoring a command with stap

SystemTap has the ability to run a module while a regular command is being run as well and ending after the command has finished.

This option is useful if your issue is related to a specific command and you want to only collect data while that command runs.
     
     # staprun -c "CMD_To_Execute" Module_Name

**Example:**
     
     root@production:~# staprun -c "wget http://...iso" ./nettop_stap.ko
     Saving to: `ubuntu-12.04-dvd-amd64.iso'
     0% [ ] 15,629,409 3.78M/s eta 8m 31s PID UID DEV XMIT_PK RECV_PK XMIT_KB RECV_KB COMMAND
      1723 105 eth0 3589 0 231 0 qemu-system-x86
      3475 0 eth0 1853 0 119 0 wget
      2583 1000 eth0 29 0 6 0 sshd
      24 0 eth0 16 0 1 0 ksmd
      1696 105 eth0 15 0 0 0 qemu-system-x86
      1723 105 vnet0 3 0 0 0 qemu-system-x86
      1723 105 vnet1 3 0 0 0 qemu-system-x86
      21 0 eth0 1 0 0 0 kworker/0:1
      3474 0 eth0 1 0 0 0 stapio

## More SystemTap Scripts

As SystemTap's user base grows and more sample scripts are developed there are large possibilities for SystemTap in the future, but we don't have to wait for then to start using its awesome features. Here is a list of [available sample scripts](http://sourceware.org/systemtap/SystemTap_Beginners_Guide/useful-systemtap-scripts.html) that I feel are incredibly useful for any Systems Administrator.

**Networking:**
	
  * `nettop.stp` - A Network Top-style command script that shows the top applications using network at any given moment.
  * `tcp_connections.stp` - A script that monitors all incoming tcp connections and prints port, cmd, pid, and source ip every time a new connection is established
  * `tcpdumplike.stp` - A very cool script that gives a summary view of your current tcp connections

**Disk & I/O:**
	
  * `disktop.stp` - Similar to iotop but a some different information is presented
  * `iotime.stp` - Tracks the i/o time for each file, it also prints the command and pid of the process making the system calls.
  * `traceio.stp` - Prints a top ten style list of the top processes who utilize i/o traffic over time
  * `inodewatch.stp` - When given a specific files information this script can monitor all read and write access to a specific inode.
  * `inodewatch2.stp` - Similar to inodewatch.stp except this script monitors attribute changes like permissions.

**CPU & System:**
	
  * `tread-times.stp` - A cpu top that is specifically for the top threads running on the server
  * `topsys.stp` - A monitor for counting frequent system calls.
  * `syscalls_by_pid.stp` - Monitor frequent system calls for a specific pid

All of these scripts are available on the SystemTap website and are immediately useful without any modification or knowledge of SystemTap's coding language.

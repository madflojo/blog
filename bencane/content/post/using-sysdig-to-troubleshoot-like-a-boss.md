---
authors:
- Benjamin Cane
categories:
- Linux
- Troubleshooting
date: '2014-04-18T09:30:00'
description: An introduction to sysdig, a new tool for advanced system troubleshooting.
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- sysdig
- systemtap
- dtrace
- strace
title: Using sysdig to Troubleshoot like a boss
url: /2014/04/18/using-sysdig-to-troubleshoot-like-a-boss

---

If you haven't seen it yet there is a new troubleshooting tool out called `sysdig`. It's been touted as `strace` meets `tcpdump` and well, it seems like it is living up to the hype. I would actually rather compare `sysdig` to SystemTap meets `tcpdump`, as it has the command line syntax of `tcpdump` but the power of SystemTap.

In this article I am going to cover some basic and cool examples for `sysdig`, for a more complete list you can look over the [sysdig wiki](https://github.com/draios/sysdig/wiki/Sysdig%20Examples). However, it seems that even the `sysdig` official documentation is only scratching the surface of what can be done with `sysdig`.

## Installation

In this article we will be installing `sysdig` on Ubuntu using `apt-get`. If you are running an `rpm` based distribution you can find details on installing via `yum` on `sysdig`'s [wiki](https://github.com/draios/sysdig/wiki/How%20to%20Install%20Sysdig%20for%20Linux).

### Setting up the apt repository

To install `sysdig` via apt we will need to setup the apt repository maintained by Draios the company behind `sysdig`. We can do this by running the following `curl` commands.

    # curl -s https://s3.amazonaws.com/download.draios.com/DRAIOS-GPG-KEY.public | apt-key add -  
    # curl -s -o /etc/apt/sources.list.d/draios.list http://download.draios.com/stable/deb/draios.list 

The first command above will download the Draios gpg key and add it to apt's key repository. The second will download an apt sources file from Draios and place it into the `/etc/apt/sources.list.d/` directory.

#### Update apt's indexes

Once the sources list and gpg key are installed we will need to re-sync apt's package indexes, this can be done by running `apt-get update`.

    # apt-get update

### Kernel headers package

The `sysdig` utility requires the kernel headers package, before installing we will need to validate that the kernel headers package is installed.

#### Check if kernel headers is installed

The system that I am using for this example already had the kernel headers packaged installed, to validate if they are installed on your system you can use the `dpkg` command.

		# dpkg --list | grep header
		ii  linux-generic                       3.11.0.12.13                     amd64        Complete Generic Linux kernel and headers
		ii  linux-headers-3.11.0-12             3.11.0-12.19                     all          Header files related to Linux kernel version 3.11.0
		ii  linux-headers-3.11.0-12-generic     3.11.0-12.19                     amd64        Linux kernel headers for version 3.11.0 on 64 bit x86 SMP
		ii  linux-headers-generic               3.11.0.12.13                     amd64        Generic Linux kernel headers

It is important to note that the kernel headers package must be for the specific kernel version your system is running. In the output above you can see the `linux-generic` package is version 3.11.0.12 and the headers package is for 3.11.0.12. If you have multiple kernels installed you can validate which version your system is running with the `uname` command.

    # uname -r
    3.11.0-12-generic

## Installing the kernel headers package

To install the headers package for this specific kernel you can use `apt-get`. Keep in mind, you must specify the kernel version listed from `uname -r`.

    # apt-get install linux-headers-<kernel version>

**Example:**

    # apt-get install linux-headers-3.11.0-12-generic

### Installing sysdig

Now that the apt repository is setup and we have the required dependencies, we can install the `sysdig` command.

    # apt-get install sysdig

## Using sysdig

### Basic Usage

The syntax for `sysdig` is similar to `tcpdump` in particular the saving and reading of trace files. All of `sysdig`'s output can be saved to a file and read later just like `tcpdump`. This is useful if you are running a process or experiencing an issue and wanted to dig through the information later. 

#### Writing trace files

To write a file we can use the `-w` flag with sysdig and specify the file name.

**Syntax:**

    # sysdig -w <output file>

**Example:**

    # sysdig -w tracefile.dump

Like `tcpdump` the `sysdig` command can be stopped with `CTRL+C`.

#### Reading trace files

Once you have written the trace file you will need to use `sysdig` to read the file, this can be accomplished with the `-r` flag.

**Syntax:**

    # sysdig -r <output file>

**Example:**

		# sysdig -r tracefile.dump
		1 23:44:57.964150879 0 <NA> (7) > switch next=6200(sysdig) 
		2 23:44:57.966700100 0 rsyslogd (358) < read res=414 data=<6>[ 3785.473354] sysdig_probe: starting capture.<6>[ 3785.473523] sysdig_probe: 
		3 23:44:57.966707800 0 rsyslogd (358) > gettimeofday 
		4 23:44:57.966708216 0 rsyslogd (358) < gettimeofday 
		5 23:44:57.966717424 0 rsyslogd (358) > futex addr=13892708 op=133(FUTEX_PRIVATE_FLAG|FUTEX_WAKE_OP) val=1 
		6 23:44:57.966721656 0 rsyslogd (358) < futex res=1 
		7 23:44:57.966724081 0 rsyslogd (358) > gettimeofday 
		8 23:44:57.966724305 0 rsyslogd (358) < gettimeofday 
		9 23:44:57.966726254 0 rsyslogd (358) > gettimeofday 
		10 23:44:57.966726456 0 rsyslogd (358) < gettimeofday 

#### Output in ASCII

By default `sysdig` saves the files in binary, however you can use the `-A` flag to have `sysdig` output in ASCII.

**Syntax:**

    # sysdig -A

**Example:**

    # sysdig -A > /var/tmp/out.txt
    # cat /var/tmp/out.txt
    1 22:26:15.076829633 0 <NA> (7) > switch next=11920(sysdig) 

The above example will redirect the output to a file in plain text, this can be helpful if you wanted to save and review the data on a system that doesn't have `sysdig` installed.

### sysdig filters

Much like `tcpdump` the `sysdig` command has filters that allow you to filter the output to specific information. You can find a list of available filters by running `sysdig` with the `-l` flag.

**Example:**

		# sysdig -l
		
		----------------------
		Field Class: fd
		
		fd.num            the unique number identifying the file descriptor.
		fd.type           type of FD. Can be 'file', 'ipv4', 'ipv6', 'unix', 'pipe', 'e
		                  vent', 'signalfd', 'eventpoll', 'inotify' or 'signalfd'.
		fd.typechar       type of FD as a single character. Can be 'f' for file, 4 for 
		                  IPv4 socket, 6 for IPv6 socket, 'u' for unix socket, p for pi
		                  pe, 'e' for eventfd, 's' for signalfd, 'l' for eventpoll, 'i'
		                   for inotify, 'o' for uknown.
		fd.name           FD full name. If the fd is a file, this field contains the fu
		                  ll path. If the FD is a socket, this field contain the connec
		                  tion tuple.
    <truncated output>

#### Filter examples

##### Capturing a specific process

You can use the "proc.name" filter to capture all of the `sysdig` events for a specific process. In the example below I am filtering on any process named sshd.

**Example:**

		# sysdig -r tracefile.dump proc.name=sshd
		530 23:45:02.804469114 0 sshd (917) < select res=1 
		531 23:45:02.804476093 0 sshd (917) > rt_sigprocmask 
		532 23:45:02.804478942 0 sshd (917) < rt_sigprocmask 
		533 23:45:02.804479542 0 sshd (917) > rt_sigprocmask 
		534 23:45:02.804479767 0 sshd (917) < rt_sigprocmask 
		535 23:45:02.804487255 0 sshd (917) > read fd=3(<4t>10.0.0.12:55993->162.0.0.80:22) size=16384

##### Capturing all processes that open a specific file

The `fd.name` filter is used to filter events for a specific file name. This can be useful to see what processes are reading or writing a specific file or socket.

**Example:**

    # sysdig fd.name=/dev/log
    14 11:13:30.982445884 0 rsyslogd (357) < read res=414 data=<6>[  582.136312] sysdig_probe: starting capture.<6>[  582.136472] sysdig_probe: 

#### Capturing all processes that open a specific filesystem

You can also use comparison operators with filters such as **contains, =, !=, <=, >=, < and >**.

**Example:**

		# sysdig fd.name contains /etc
		8675 11:16:18.424407754 0 apache2 (1287) < open fd=13(<f>/etc/apache2/.htpasswd) name=/etc/apache2/.htpasswd flags=1(O_RDONLY) mode=0 
		8678 11:16:18.424422599 0 apache2 (1287) > fstat fd=13(<f>/etc/apache2/.htpasswd) 
		8679 11:16:18.424423601 0 apache2 (1287) < fstat res=0 
		8680 11:16:18.424427497 0 apache2 (1287) > read fd=13(<f>/etc/apache2/.htpasswd) size=4096 
		8683 11:16:18.424606422 0 apache2 (1287) < read res=44 data=admin:$apr1$OXXed8Rc$rbXNhN/VqLCP.ojKu1aUN1. 
		8684 11:16:18.424623679 0 apache2 (1287) > close fd=13(<f>/etc/apache2/.htpasswd) 
		8685 11:16:18.424625424 0 apache2 (1287) < close res=0 
		9702 11:16:21.285934861 0 apache2 (1287) < open fd=13(<f>/etc/apache2/.htpasswd) name=/etc/apache2/.htpasswd flags=1(O_RDONLY) mode=0 
		9703 11:16:21.285936317 0 apache2 (1287) > fstat fd=13(<f>/etc/apache2/.htpasswd) 
		9704 11:16:21.285937024 0 apache2 (1287) < fstat res=0 

As you can see from the above examples filters can be used for both reading from a file or the live event stream.

### Chisels

Earlier I compared `sysdig` to SystemTap, Chisels is why I made that reference. Similar tools like SystemTap have a SystemTap only scripting language that allows you to extend the functionality of SystemTap. In `sysdig` these are called chisels and they can be written in LUA which is a common programming language. I personally think the choice to use LUA was a good one, as it makes extending `sysdig` easy for newcomers.

#### List available chisels

To list the available chisels you can use the `-cl` flag with `sysdig`.

**Example:**

		# sysdig -cl
		
		Category: CPU Usage
		-------------------
		topprocs_cpu    Top processes by CPU usage
		
		Category: I/O
		-------------
		echo_fds        Print the data read and written by processes.
		fdbytes_by      I/O bytes, aggregated by an arbitrary filter field
		fdcount_by      FD count, aggregated by an arbitrary filter field
		iobytes         Sum of I/O bytes on any type of FD
		iobytes_file    Sum of file I/O bytes
		stderr          Print stderr of processes
		stdin           Print stdin of processes
		stdout          Print stdout of processes
		<truncated output>

The list is fairly long even though `sysdig` is still pretty new, and since `sysdig` is on [GitHub](https://github.com/draios/sysdig) you can easily contribute and extend `sysdig` with your own chisels.

#### Display chisel information

While the list command gives a small description of the chisels you can display more information using the `-i` flag with the chisel name.

**Example:**

		# sysdig -i bottlenecks
		
		Category: Performance
		---------------------
		bottlenecks     Slowest system calls
		
		Use the -i flag to get detailed information about a specific chisel
		
		Lists the 10 system calls that took the longest to return dur
		ing the capture interval.
		
		Args:
		(None)

#### Running a chisel

To run a chisel you can run `sysdig` with the `-c` flag and specify the chisel name.

**Example:**

		# sysdig -c topprocs_net
		Bytes     Process
		------------------------------
		296B      sshd

#### Running a chisel with filters

Even with chisels you can still use filters to run chisels against specific events. 

#### Capturing all network traffic from a specific process

The below example shows using the `echo_fds` chisel against the processes named **apache2**.

    # sysdig -A -c echo_fds proc.name=apache2
    ------ Read 444B from 127.0.0.1:57793->162.243.109.80:80

    GET /wp-admin/install.php HTTP/1.1
    Host: 162.243.109.80
    Connection: keep-alive
    Cache-Control: max-age=0
    Authorization: Basic YWRtaW46ZUNCM3lyZmRRcg==
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36
    Accept-Encoding: gzip,deflate,sdch
    Accept-Language: en-US,en;q=0.8

#### Capturing network traffic exchanged between a specific ip

We can also use the the `echo_fds` chisel to show all network traffic for a single ip using the `fd.cip` filter. 

    # sysdig -A -c echo_fds fd.cip=127.0.0.1
    ------ Write 1.92KB to 127.0.0.1:58896->162.243.109.80:80

    HTTP/1.1 200 OK
    Date: Thu, 17 Apr 2014 03:11:33 GMT
    Server: Apache
    X-Powered-By: PHP/5.5.3-1ubuntu2.3
    Vary: Accept-Encoding
    Content-Encoding: gzip
    Content-Length: 1698
    Keep-Alive: timeout=5, max=100
    Connection: Keep-Alive
    Content-Type: text/html; charset=utf-8

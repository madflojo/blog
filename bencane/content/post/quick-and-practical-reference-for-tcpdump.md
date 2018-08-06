---
authors:
- Benjamin Cane
categories:
- Linux
- Networking
- Troubleshooting
date: '2014-10-13T14:50:00'
description: This article is a quick and practical reference for tcpdump, it covers
  the basics and dives a little bit into advanced usage. This article should cover
  everything a systems or network administrator needs to get started and troubleshoot
  issues quickly
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- unix
- tcpdump
- network troubleshooting
- linux network troubleshooting
- packet capture
title: A Quick and Practical Reference for tcpdump
url: /2014/10/13/quick-and-practical-reference-for-tcpdump

---

When it comes to `tcpdump` most admins fall into two categories; they either know `tcpdump` and all of its flags like the back of their hand, or they kind of know it but need to use a reference for anything outside of the basic usage. The reason for this is because `tcpdump` is a pretty advanced command and it is pretty easy to get into the depths of how networking works when using it.

For today's article I wanted to create a quick but practical reference for `tcpdump`. I will cover the basics as well as some of the more advanced usage. I am sure I will most likely leave out some cool commands so if you want to add anything please feel free to drop it into the comments section.

Before we get too far into the weeds, it is probably best to cover what `tcpdump` is used for. The command `tcpdump` is used to create "dumps" or "traces" of network traffic. It allows you to look at what is happening on the network and really can be useful for troubleshooting many types of issues including issues that aren't due to network communications. Outside of network issues I use `tcpdump` to troubleshoot application issues all the time; if you ever have two applications that don't seem to be working well together, `tcpdump` is a great way to see what is happening. This is especially true if the traffic is not encrypted as `tcpdump` can be used to capture and read packet data as well.

## The Basics

The first thing to cover with `tcpdump` is what flags to use. In this section I am going to cover the most basic flags that can be used in most situations.

### Don't translate hostnames, ports, etc

    # tcpdump -n

By default `tcpdump` will try to lookup and translate hostnames and ports.

    # tcpdump
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on eth0, link-type EN10MB (Ethernet), capture size 65535 bytes
    16:15:05.051896 IP blog.ssh > 10.0.3.1.32855: Flags [P.], seq 2546456553:2546456749, ack 1824683693, win 355, options [nop,nop,TS val 620879437 ecr 620879348], length 196

You can turn this off by using the `-n` flag. Personally, I always use this flag as the hostname and port translation usually annoys me because I tend to work from IP addresses rather than hostnames. However, knowing that you can have `tcpdump` translate or not translate these are useful; as there are times where knowing what server the source traffic is coming from is important.

    # tcpdump -n
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on eth0, link-type EN10MB (Ethernet), capture size 65535 bytes
    16:23:47.934665 IP 10.0.3.246.22 > 10.0.3.1.32855: Flags [P.], seq 2546457621:2546457817, ack 1824684201, win 355, options [nop,nop,TS val 621010158 ecr 621010055], length 196

### Adding verbosity

    # tcpdump -v

By adding a simple `-v` the output will start including a bit more such as the ttl, total length and options in an the IP packets.

    # tcpdump
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on eth0, link-type EN10MB (Ethernet), capture size 65535 bytes
    16:15:05.051896 IP blog.ssh > 10.0.3.1.32855: Flags [P.], seq 2546456553:2546456749, ack 1824683693, win 355, options [nop,nop,TS val 620879437 ecr 620879348], length 196

`tcpdump` has three verbosity levels, you can add more verbosity by adding additional `v`'s to the command line flags. In general whenever I am using `tcpdump` I tend to use the highest verbosity, as I like having everything visible just in case I need it.

    # tcpdump -vvv -c 1
    tcpdump: listening on eth0, link-type EN10MB (Ethernet), capture size 65535 bytes
    16:36:13.873456 IP (tos 0x10, ttl 64, id 121, offset 0, flags [DF], proto TCP (6), length 184)
        blog.ssh > 10.0.3.1.32855: Flags [P.], cksum 0x1ba1 (incorrect -> 0x0dfd), seq 2546458841:2546458973, ack 1824684869, win 355, options [nop,nop,TS val 621196643 ecr 621196379], length 132

### Specifying an Interface

    # tcpdump -i eth0

By default when you run `tcpdump` without specifying an interface it will choose the lowest numbered interface, usually this is `eth0` however that is not guaranteed for all systems.

    # tcpdump
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on eth0, link-type EN10MB (Ethernet), capture size 65535 bytes
    16:15:05.051896 IP blog.ssh > 10.0.3.1.32855: Flags [P.], seq 2546456553:2546456749, ack 1824683693, win 355, options [nop,nop,TS val 620879437 ecr 620879348], length 196

You can specify the interface by using the `-i` flag followed by the interface name. On most linux systems a special interface name of `any` can be used to tell `tcpdump` to listen on all interfaces, I find this extremely useful when troubleshooting servers with multiple interfaces. This is especially true when there are routing issues involved.

    # tcpdump -i any
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on any, link-type LINUX_SLL (Linux cooked), capture size 65535 bytes
    16:45:59.312046 IP blog.ssh > 10.0.3.1.32855: Flags [P.], seq 2547763641:2547763837, ack 1824693949, win 355, options [nop,nop,TS val 621343002 ecr 621342962], length 196

### Writing to a file

    # tcpdump -w /path/to/file

When you just run `tcpdump` by itself it will output to your screen.

    # tcpdump
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on eth0, link-type EN10MB (Ethernet), capture size 65535 bytes
    16:15:05.051896 IP blog.ssh > 10.0.3.1.32855: Flags [P.], seq 2546456553:2546456749, ack 1824683693, win 355, options [nop,nop,TS val 620879437 ecr 620879348], length 196

There are many times where you may want to save the `tcpdump` data to a file, the easiest way to do this is to use the `-w` flag. This is useful for situations where you may need to save the network dump to review later. One benefit to saving the data to a file is that you can read the dump file multiple times and apply other flags or filters (which we will cover below) to that snapshot of network traffic.

    # tcpdump -w /var/tmp/tcpdata.pcap
    tcpdump: listening on eth0, link-type EN10MB (Ethernet), capture size 65535 bytes
    1 packet captured
    2 packets received by filter
    0 packets dropped by kernel

By default the data is buffered and will not usually be written to the file until you `CTRL+C` out of the running `tcpdump` command.

### Reading from a file

    # tcpdump -r /path/to/file

Once you save the output to a file you will inherently need to read that file. To do this you can simply use the `-r` flag followed by the path to the file.

    # tcpdump -r /var/tmp/tcpdata.pcap 
    reading from file /var/tmp/tcpdata.pcap, link-type EN10MB (Ethernet)
    16:56:01.610473 IP blog.ssh > 10.0.3.1.32855: Flags [P.], seq 2547766673:2547766805, ack 1824696181, win 355, options [nop,nop,TS val 621493577 ecr 621493478], length 132

As a quick note, if you are more familiar with tools such as [wireshark](https://www.wireshark.org) you can read files saved by `tcpdump` with most network troubleshooting tools like wireshark.

### Specifying the capture size of each packet

    # tcpdump -s 100

By default most newer implementations of `tcpdump` will capture **65535** bytes, however in some situations you may not want to capture the default packet length. You can use `-s` to specify the "snaplen" or "snapshot length" that you want `tcpdump` to capture.

### Specifying the number of packets to capture

    # tcpdump -c 10

When you run `tcpdump` by itself it will keep running until you hit `CTRL+C` to quit. 

    # tcpdump host google.com
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on eth0, link-type EN10MB (Ethernet), capture size 65535 bytes
    ^C
    0 packets captured
    4 packets received by filter
    0 packets dropped by kernel

You can tell `tcpdump` to stop capturing after a certain number of packets by using the `-c` flag followed by the number of packets to capture. This is pretty useful for situations where you may not want `tcpdump` to spew output to your screen so fast you can't read it, however generally this is more useful when you are using filters to grab specific traffic.

### Pulling the basics together

    # tcpdump -nvvv -i any -c 100 -s 100

All of the basic flags that were covered above can also be combined to allow you to specify exactly what you want tcpdump to provide.

    # tcpdump -w /var/tmp/tcpdata.pcap -i any -c 10 -vvv
    tcpdump: listening on any, link-type LINUX_SLL (Linux cooked), capture size 65535 bytes
    10 packets captured
    10 packets received by filter
    0 packets dropped by kernel
    # tcpdump -r /var/tmp/tcpdata.pcap -nvvv -c 5
    reading from file /var/tmp/tcpdata.pcap, link-type LINUX_SLL (Linux cooked)
    17:35:14.465902 IP (tos 0x10, ttl 64, id 5436, offset 0, flags [DF], proto TCP (6), length 104)
        10.0.3.246.22 > 10.0.3.1.32855: Flags [P.], cksum 0x1b51 (incorrect -> 0x72bc), seq 2547781277:2547781329, ack 1824703573, win 355, options [nop,nop,TS val 622081791 ecr 622081775], length 52
    17:35:14.466007 IP (tos 0x10, ttl 64, id 52193, offset 0, flags [DF], proto TCP (6), length 52)
        10.0.3.1.32855 > 10.0.3.246.22: Flags [.], cksum 0x1b1d (incorrect -> 0x4950), seq 1, ack 52, win 541, options [nop,nop,TS val 622081791 ecr 622081791], length 0
    17:35:14.470239 IP (tos 0x10, ttl 64, id 5437, offset 0, flags [DF], proto TCP (6), length 168)
        10.0.3.246.22 > 10.0.3.1.32855: Flags [P.], cksum 0x1b91 (incorrect -> 0x98c3), seq 52:168, ack 1, win 355, options [nop,nop,TS val 622081792 ecr 622081791], length 116
    17:35:14.470370 IP (tos 0x10, ttl 64, id 52194, offset 0, flags [DF], proto TCP (6), length 52)
        10.0.3.1.32855 > 10.0.3.246.22: Flags [.], cksum 0x1b1d (incorrect -> 0x48da), seq 1, ack 168, win 541, options [nop,nop,TS val 622081792 ecr 622081792], length 0
    17:35:15.464575 IP (tos 0x10, ttl 64, id 5438, offset 0, flags [DF], proto TCP (6), length 104)
        10.0.3.246.22 > 10.0.3.1.32855: Flags [P.], cksum 0x1b51 (incorrect -> 0xc3ba), seq 168:220, ack 1, win 355, options [nop,nop,TS val 622082040 ecr 622081792], length 52

## Filters

Now that we have covered some of the basic flags we should cover filtering. `tcpdump` has the ability to filter the capture or output based on a variety of expressions, in this article I am only going to cover a few quick examples to give you an idea of the syntax. For a full list you can checkout the [pcap-filter](http://www.tcpdump.org/manpages/pcap-filter.7.html) section of the `tcpdump` manpage.

### Searching for traffic to and from a specific host

    # tcpdump -nvvv -i any -c 3 host 10.0.3.1

The above command will run a `tcpdump` and send the output to the screen like we saw with the flags before, however it will only do so if the `source` or `destination` IP address is `10.0.3.1`. Essentially by adding `host 10.0.3.1` we are asking tcpdump to filter out anything that is not to or from `10.0.3.1`.

    # tcpdump -nvvv -i any -c 3 host 10.0.3.1
    tcpdump: listening on any, link-type LINUX_SLL (Linux cooked), capture size 65535 bytes
    17:54:15.067496 IP (tos 0x10, ttl 64, id 5502, offset 0, flags [DF], proto TCP (6), length 184)
        10.0.3.246.22 > 10.0.3.1.32855: Flags [P.], cksum 0x1ba1 (incorrect -> 0x9f75), seq 2547785621:2547785753, ack 1824705637, win 355, options [nop,nop,TS val 622366941 ecr 622366923], length 132
    17:54:15.067613 IP (tos 0x10, ttl 64, id 52315, offset 0, flags [DF], proto TCP (6), length 52)
        10.0.3.1.32855 > 10.0.3.246.22: Flags [.], cksum 0x1b1d (incorrect -> 0x7c34), seq 1, ack 132, win 540, options [nop,nop,TS val 622366941 ecr 622366941], length 0
    17:54:15.075230 IP (tos 0x10, ttl 64, id 5503, offset 0, flags [DF], proto TCP (6), length 648)
        10.0.3.246.22 > 10.0.3.1.32855: Flags [P.], cksum 0x1d71 (incorrect -> 0x3443), seq 132:728, ack 1, win 355, options [nop,nop,TS val 622366943 ecr 622366941], length 596

### Only show traffic where the source is a specific host

    # tcpdump -nvvv -i any -c 3 src host 10.0.3.1

Where the previous example showed traffic to and from `10.0.3.1` the above command will only show traffic where the source of the packet is `10.0.3.1`. This is accomplished by adding `src` in front of the `host` filter. This is an additional filter that tells `tcpdump` to look for a specific "source". This can be reversed by using the `dst` filter, which specifies the "destination".

    # tcpdump -nvvv -i any -c 3 src host 10.0.3.1
    tcpdump: listening on any, link-type LINUX_SLL (Linux cooked), capture size 65535 bytes
    17:57:12.194902 IP (tos 0x10, ttl 64, id 52357, offset 0, flags [DF], proto TCP (6), length 52)
        10.0.3.1.32855 > 10.0.3.246.22: Flags [.], cksum 0x1b1d (incorrect -> 0x1707), seq 1824706545, ack 2547787717, win 540, options [nop,nop,TS val 622411223 ecr 622411223], length 0
    17:57:12.196288 IP (tos 0x10, ttl 64, id 52358, offset 0, flags [DF], proto TCP (6), length 52)
        10.0.3.1.32855 > 10.0.3.246.22: Flags [.], cksum 0x1b1d (incorrect -> 0x15c5), seq 0, ack 325, win 538, options [nop,nop,TS val 622411223 ecr 622411223], length 0
    17:57:12.197677 IP (tos 0x10, ttl 64, id 52359, offset 0, flags [DF], proto TCP (6), length 52)
        10.0.3.1.32855 > 10.0.3.246.22: Flags [.], cksum 0x1b1d (incorrect -> 0x1491), seq 0, ack 633, win 536, options [nop,nop,TS val 622411224 ecr 622411224], length 0
    # tcpdump -nvvv -i any -c 3 dst host 10.0.3.1
    tcpdump: listening on any, link-type LINUX_SLL (Linux cooked), capture size 65535 bytes
    17:59:37.266838 IP (tos 0x10, ttl 64, id 5552, offset 0, flags [DF], proto TCP (6), length 184)
        10.0.3.246.22 > 10.0.3.1.32855: Flags [P.], cksum 0x1ba1 (incorrect -> 0x586d), seq 2547789725:2547789857, ack 1824707577, win 355, options [nop,nop,TS val 622447491 ecr 622447471], length 132
    17:59:37.267850 IP (tos 0x10, ttl 64, id 5553, offset 0, flags [DF], proto TCP (6), length 392)
        10.0.3.246.22 > 10.0.3.1.32855: Flags [P.], cksum 0x1c71 (incorrect -> 0x462e), seq 132:472, ack 1, win 355, options [nop,nop,TS val 622447491 ecr 622447491], length 340
    17:59:37.268606 IP (tos 0x10, ttl 64, id 5554, offset 0, flags [DF], proto TCP (6), length 360)
        10.0.3.246.22 > 10.0.3.1.32855: Flags [P.], cksum 0x1c51 (incorrect -> 0xf469), seq 472:780, ack 1, win 355, options [nop,nop,TS val 622447491 ecr 622447491], length 308

### Filtering source and destination ports

    # tcpdump -nvvv -i any -c 3 port 22 and port 60738

You can add some rather complicated filtering statements with `tcpdump` when you start to using operators like `and`. You can think of this as something similar to if statements. In this example we are using the `and` operator to tell `tcpdump` to only output packets that have both ports `22` and `60738`. This allows us to narrow down the packets to a specific session, this can be extremely useful when troubleshooting network issues.

    # tcpdump -nvvv -i any -c 3 port 22 and port 60738
    tcpdump: listening on any, link-type LINUX_SLL (Linux cooked), capture size 65535 bytes
    18:05:54.069403 IP (tos 0x10, ttl 64, id 64401, offset 0, flags [DF], proto TCP (6), length 104)
        10.0.3.1.60738 > 10.0.3.246.22: Flags [P.], cksum 0x1b51 (incorrect -> 0x5b3c), seq 917414532:917414584, ack 1550997318, win 353, options [nop,nop,TS val 622541691 ecr 622538903], length 52
    18:05:54.072963 IP (tos 0x10, ttl 64, id 13601, offset 0, flags [DF], proto TCP (6), length 184)
        10.0.3.246.22 > 10.0.3.1.60738: Flags [P.], cksum 0x1ba1 (incorrect -> 0xb0b1), seq 1:133, ack 52, win 355, options [nop,nop,TS val 622541692 ecr 622541691], length 132
    18:05:54.073080 IP (tos 0x10, ttl 64, id 64402, offset 0, flags [DF], proto TCP (6), length 52)
        10.0.3.1.60738 > 10.0.3.246.22: Flags [.], cksum 0x1b1d (incorrect -> 0x1e3b), seq 52, ack 133, win 353, options [nop,nop,TS val 622541692 ecr 622541692], length 0

You can express the `and` operator in a couple of different ways, you can use `and` or `&&`. Personally, I tend to use them both; it is important to remember that if you are going to use `&&` that you should enclose the filter expression with single or double quotes. In BASH you can use `&&` to run one command and if successful run a second. In general it is best to simply wrap filter expressions in quotes; this will prevent any unexpected results as filters can have quite a few special characters.

    # tcpdump -nvvv -i any -c 3 'port 22 && port 60738'
    tcpdump: listening on any, link-type LINUX_SLL (Linux cooked), capture size 65535 bytes
    18:06:16.062818 IP (tos 0x10, ttl 64, id 64405, offset 0, flags [DF], proto TCP (6), length 88)
        10.0.3.1.60738 > 10.0.3.246.22: Flags [P.], cksum 0x1b41 (incorrect -> 0x776c), seq 917414636:917414672, ack 1550997518, win 353, options [nop,nop,TS val 622547190 ecr 622541776], length 36
    18:06:16.065567 IP (tos 0x10, ttl 64, id 13603, offset 0, flags [DF], proto TCP (6), length 120)
        10.0.3.246.22 > 10.0.3.1.60738: Flags [P.], cksum 0x1b61 (incorrect -> 0xaf2d), seq 1:69, ack 36, win 355, options [nop,nop,TS val 622547191 ecr 622547190], length 68
    18:06:16.065696 IP (tos 0x10, ttl 64, id 64406, offset 0, flags [DF], proto TCP (6), length 52)
        10.0.3.1.60738 > 10.0.3.246.22: Flags [.], cksum 0x1b1d (incorrect -> 0xf264), seq 36, ack 69, win 353, options [nop,nop,TS val 622547191 ecr 622547191], length 0

### Searching for traffic on one port or another


    # tcpdump -nvvv -i any -c 20 'port 80 or port 443'

You can also use the `or` or `||` operator to filter `tcpdump` results. In this example we are using the `or` operator to capture traffic to and from port `80` or port `443`. This example is especially useful as webservers generally have two ports open, `80` for `http` traffic and `443` for `https`. 

    # tcpdump -nvvv -i any -c 20 'port 80 or port 443'
    tcpdump: listening on any, link-type LINUX_SLL (Linux cooked), capture size 65535 bytes
    18:24:28.817940 IP (tos 0x0, ttl 64, id 39930, offset 0, flags [DF], proto TCP (6), length 60)
        10.0.3.1.50524 > 10.0.3.246.443: Flags [S], cksum 0x1b25 (incorrect -> 0x8611), seq 3836995553, win 29200, options [mss 1460,sackOK,TS val 622820379 ecr 0,nop,wscale 7], length 0
    18:24:28.818052 IP (tos 0x0, ttl 64, id 0, offset 0, flags [DF], proto TCP (6), length 40)
        10.0.3.246.443 > 10.0.3.1.50524: Flags [R.], cksum 0x012c (correct), seq 0, ack 3836995554, win 0, length 0
    18:24:32.721330 IP (tos 0x0, ttl 64, id 48510, offset 0, flags [DF], proto TCP (6), length 475)
        10.0.3.1.60374 > 10.0.3.246.80: Flags [P.], cksum 0x1cc4 (incorrect -> 0x3a4e), seq 580573019:580573442, ack 1982754038, win 237, options [nop,nop,TS val 622821354 ecr 622815632], length 423
    18:24:32.721465 IP (tos 0x0, ttl 64, id 1266, offset 0, flags [DF], proto TCP (6), length 52)
        10.0.3.246.80 > 10.0.3.1.60374: Flags [.], cksum 0x1b1d (incorrect -> 0x45d7), seq 1, ack 423, win 243, options [nop,nop,TS val 622821355 ecr 622821354], length 0
    18:24:32.722098 IP (tos 0x0, ttl 64, id 1267, offset 0, flags [DF], proto TCP (6), length 241)
        10.0.3.246.80 > 10.0.3.1.60374: Flags [P.], cksum 0x1bda (incorrect -> 0x855c), seq 1:190, ack 423, win 243, options [nop,nop,TS val 622821355 ecr 622821354], length 189
    18:24:32.722232 IP (tos 0x0, ttl 64, id 48511, offset 0, flags [DF], proto TCP (6), length 52)
        10.0.3.1.60374 > 10.0.3.246.80: Flags [.], cksum 0x1b1d (incorrect -> 0x4517), seq 423, ack 190, win 245, options [nop,nop,TS val 622821355 ecr 622821355], length 0

### Searching for traffic on two specific ports and from a specific host

    # tcpdump -nvvv -i any -c 20 '(port 80 or port 443) and host 10.0.3.169'

While the previous example is great for looking at issues for a multiport protocol; what if this is a very high traffic webserver? The output from `tcpdump` may get a bit confusing. We can narrow down the results even further by adding a `host` filter. To do this while maintaining our `or` expression we can simply wrap the `or` statement in parenthesis. 

    # tcpdump -nvvv -i any -c 20 '(port 80 or port 443) and host 10.0.3.169'
    tcpdump: listening on any, link-type LINUX_SLL (Linux cooked), capture size 65535 bytes
    18:38:05.551194 IP (tos 0x0, ttl 64, id 63169, offset 0, flags [DF], proto TCP (6), length 60)
        10.0.3.169.33786 > 10.0.3.246.443: Flags [S], cksum 0x1bcd (incorrect -> 0x0d96), seq 4173164403, win 29200, options [mss 1460,sackOK,TS val 623024562 ecr 0,nop,wscale 7], length 0
    18:38:05.551310 IP (tos 0x0, ttl 64, id 0, offset 0, flags [DF], proto TCP (6), length 40)
        10.0.3.246.443 > 10.0.3.169.33786: Flags [R.], cksum 0xa64a (correct), seq 0, ack 4173164404, win 0, length 0
    18:38:05.717130 IP (tos 0x0, ttl 64, id 51574, offset 0, flags [DF], proto TCP (6), length 60)
        10.0.3.169.35629 > 10.0.3.246.80: Flags [S], cksum 0x1bcd (incorrect -> 0xdf7c), seq 1068257453, win 29200, options [mss 1460,sackOK,TS val 623024603 ecr 0,nop,wscale 7], length 0
    18:38:05.717255 IP (tos 0x0, ttl 64, id 0, offset 0, flags [DF], proto TCP (6), length 60)
        10.0.3.246.80 > 10.0.3.169.35629: Flags [S.], cksum 0x1bcd (incorrect -> 0xed80), seq 2992472447, ack 1068257454, win 28960, options [mss 1460,sackOK,TS val 623024603 ecr 623024603,nop,wscale 7], length 0
    18:38:05.717474 IP (tos 0x0, ttl 64, id 51575, offset 0, flags [DF], proto TCP (6), length 52)
        10.0.3.169.35629 > 10.0.3.246.80: Flags [.], cksum 0x1bc5 (incorrect -> 0x8c87), seq 1, ack 1, win 229, options [nop,nop,TS val 623024604 ecr 623024603], length 0

You can use the parenthesis multiple times in a single filter, for example the below command will filter the capture to only packets that are to or from port `80` or port `443` and from hosts `10.0.3.169` and `10.0.3.1` if they are destined for `10.0.3.246`.

    # tcpdump -nvvv -i any -c 20 '((port 80 or port 443) and (host 10.0.3.169 or host 10.0.3.1)) and dst host 10.0.3.246'
    tcpdump: listening on any, link-type LINUX_SLL (Linux cooked), capture size 65535 bytes
    18:53:30.349306 IP (tos 0x0, ttl 64, id 52641, offset 0, flags [DF], proto TCP (6), length 60)
        10.0.3.1.35407 > 10.0.3.246.80: Flags [S], cksum 0x1b25 (incorrect -> 0x4890), seq 3026316656, win 29200, options [mss 1460,sackOK,TS val 623255761 ecr 0,nop,wscale 7], length 0
    18:53:30.349558 IP (tos 0x0, ttl 64, id 52642, offset 0, flags [DF], proto TCP (6), length 52)
        10.0.3.1.35407 > 10.0.3.246.80: Flags [.], cksum 0x1b1d (incorrect -> 0x3454), seq 3026316657, ack 3657995297, win 229, options [nop,nop,TS val 623255762 ecr 623255762], length 0
    18:53:30.354056 IP (tos 0x0, ttl 64, id 52643, offset 0, flags [DF], proto TCP (6), length 475)
        10.0.3.1.35407 > 10.0.3.246.80: Flags [P.], cksum 0x1cc4 (incorrect -> 0x10c2), seq 0:423, ack 1, win 229, options [nop,nop,TS val 623255763 ecr 623255762], length 423
    18:53:30.354682 IP (tos 0x0, ttl 64, id 52644, offset 0, flags [DF], proto TCP (6), length 52)
        10.0.3.1.35407 > 10.0.3.246.80: Flags [.], cksum 0x1b1d (incorrect -> 0x31e6), seq 423, ack 190, win 237, options [nop,nop,TS val 623255763 ecr 623255763], length 0

## Understanding the output

Capturing network traffic with `tcpdump` is hard enough with all of the options, but once you have that data you have to decipher it. In this section we are going to cover how to identify the source/destination IP, source/destination Port and the type of packet for the TCP protocol. While these are all very basic items they are far from the extent of what you can identify from `tcpdump`, however this article is meant to be quick and dirty so we will keep it to the basics. For more information on `tcpdump` and what is being listed I suggest checking out the [manpages](http://www.tcpdump.org/manpages/).

### Identifying the source and destination

Identifying the source and destination addresses and ports are actually fairly easy. 

    10.0.3.246.56894 > 192.168.0.92.22: Flags [S], cksum 0xcf28 (incorrect -> 0x0388), seq 682725222, win 29200, options [mss 1460,sackOK,TS val 619989005 ecr 0,nop,wscale 7], length 0

Given the above output we can see that the source ip is `10.0.3.246` the source port is `56894` and the destination ip is `192.168.0.92` with a destination port of `22`. This is pretty easy to identify once you understand the format of `tcpdump`. If you haven't guessed the format yet you can break it down as follows `src-ip.src-port > dest-ip.dest-port: Flags[S]` the source is in front of the `>` and the destination is behind. You can think of the `>` as an arrow pointing to the destination.

### Identifying the type of packet

    10.0.3.246.56894 > 192.168.0.92.22: Flags [S], cksum 0xcf28 (incorrect -> 0x0388), seq 682725222, win 29200, options [mss 1460,sackOK,TS val 619989005 ecr 0,nop,wscale 7], length 0

From the sample above we can tell that the packet is a single `SYN` packet. We can identify this by the `Flags [S]` section of the `tcpdump` output, different types of packets have different types of flags. Without going too deep into what types of packets exist within TCP you can use the below as a cheat sheet for identifying packet types.

* `[S]` - SYN (Start Connection)
* `[.]` - No Flag Set
* `[P]` - PSH (Push Data)
* `[F]` - FIN (Finish Connection)
* `[R]` - RST (Reset Connection)

Depending on the version and output of tcpdump you may also see flags such as `[S.]` this is used to indicate a `SYN-ACK` packet.

#### An unhealthy example

    15:15:43.323412 IP (tos 0x0, ttl 64, id 51051, offset 0, flags [DF], proto TCP (6), length 60)
        10.0.3.246.56894 > 192.168.0.92.22: Flags [S], cksum 0xcf28 (incorrect -> 0x0388), seq 682725222, win 29200, options [mss 1460,sackOK,TS val 619989005 ecr 0,nop,wscale 7], length 0
    15:15:44.321444 IP (tos 0x0, ttl 64, id 51052, offset 0, flags [DF], proto TCP (6), length 60)
        10.0.3.246.56894 > 192.168.0.92.22: Flags [S], cksum 0xcf28 (incorrect -> 0x028e), seq 682725222, win 29200, options [mss 1460,sackOK,TS val 619989255 ecr 0,nop,wscale 7], length 0
    15:15:46.321610 IP (tos 0x0, ttl 64, id 51053, offset 0, flags [DF], proto TCP (6), length 60)
        10.0.3.246.56894 > 192.168.0.92.22: Flags [S], cksum 0xcf28 (incorrect -> 0x009a), seq 682725222, win 29200, options [mss 1460,sackOK,TS val 619989755 ecr 0,nop,wscale 7], length 0

The above sampling shows an example of an unhealthy exchange, and by unhealthy exchange for this example that means no exchange. In the above sample we can see that `10.0.3.246` is sending a `SYN` packet to host `192.168.0.92` however we never see a response from host `192.168.0.92`.


#### A healthy example

    15:18:25.716453 IP (tos 0x10, ttl 64, id 53344, offset 0, flags [DF], proto TCP (6), length 60)
        10.0.3.246.34908 > 192.168.0.110.22: Flags [S], cksum 0xcf3a (incorrect -> 0xc838), seq 1943877315, win 29200, options [mss 1460,sackOK,TS val 620029603 ecr 0,nop,wscale 7], length 0
    15:18:25.716777 IP (tos 0x0, ttl 63, id 0, offset 0, flags [DF], proto TCP (6), length 60)
        192.168.0.110.22 > 10.0.3.246.34908: Flags [S.], cksum 0x594a (correct), seq 4001145915, ack 1943877316, win 5792, options [mss 1460,sackOK,TS val 18495104 ecr 620029603,nop,wscale 2], length 0
    15:18:25.716899 IP (tos 0x10, ttl 64, id 53345, offset 0, flags [DF], proto TCP (6), length 52)
        10.0.3.246.34908 > 192.168.0.110.22: Flags [.], cksum 0xcf32 (incorrect -> 0x9dcc), ack 1, win 229, options [nop,nop,TS val 620029603 ecr 18495104], length 0

A healthy example would look like the above, in the above we can see a standard TCP 3-way handshake. The first packet above is a `SYN` packet from host `10.0.3.246` to host `192.168.0.110`, the second packet is a `SYN-ACK` from host `192.168.0.110` acknowledging the `SYN`. The final packet is a `ACK` or rather a `SYN-ACK-ACK` from host `10.0.3.246` acknowledging that it has received the `SYN-ACK`. From this point on there is an established TCP/IP connection. 

## Packet Inspection

### Printing packet data in Hex and ASCII

    # tcpdump -nvvv -i any -c 1 -XX 'port 80 and host 10.0.3.1'

A common method of troubleshooting application issues over the network is by using `tcpdump` to use the `-XX` flag to print the packet data in hex and ascii. This is a pretty helpful command, it allows you to look at both the source, destination, type of packet and the packet itself. However, I am not a fan of this output. I think it is a bit hard to read.

    # tcpdump -nvvv -i any -c 1 -XX 'port 80 and host 10.0.3.1'
    tcpdump: listening on any, link-type LINUX_SLL (Linux cooked), capture size 65535 bytes
    19:51:15.697640 IP (tos 0x0, ttl 64, id 54313, offset 0, flags [DF], proto TCP (6), length 483)
        10.0.3.1.45732 > 10.0.3.246.80: Flags [P.], cksum 0x1ccc (incorrect -> 0x2ce8), seq 3920159713:3920160144, ack 969855140, win 245, options [nop,nop,TS val 624122099 ecr 624117334], length 431
            0x0000:  0000 0001 0006 fe0a e2d1 8785 0000 0800  ................
            0x0010:  4500 01e3 d429 4000 4006 49f5 0a00 0301  E....)@.@.I.....
            0x0020:  0a00 03f6 b2a4 0050 e9a8 e3e1 39ce d0a4  .......P....9...
            0x0030:  8018 00f5 1ccc 0000 0101 080a 2533 58f3  ............%3X.
            0x0040:  2533 4656 4745 5420 2f73 6f6d 6570 6167  %3FVGET./somepag
            0x0050:  6520 4854 5450 2f31 2e31 0d0a 486f 7374  e.HTTP/1.1..Host
            0x0060:  3a20 3130 2e30 2e33 2e32 3436 0d0a 436f  :.10.0.3.246..Co
            0x0070:  6e6e 6563 7469 6f6e 3a20 6b65 6570 2d61  nnection:.keep-a
            0x0080:  6c69 7665 0d0a 4361 6368 652d 436f 6e74  live..Cache-Cont
            0x0090:  726f 6c3a 206d 6178 2d61 6765 3d30 0d0a  rol:.max-age=0..
            0x00a0:  4163 6365 7074 3a20 7465 7874 2f68 746d  Accept:.text/htm
            0x00b0:  6c2c 6170 706c 6963 6174 696f 6e2f 7868  l,application/xh
            0x00c0:  746d 6c2b 786d 6c2c 6170 706c 6963 6174  tml+xml,applicat
            0x00d0:  696f 6e2f 786d 6c3b 713d 302e 392c 696d  ion/xml;q=0.9,im
            0x00e0:  6167 652f 7765 6270 2c2a 2f2a 3b71 3d30  age/webp,*/*;q=0
            0x00f0:  2e38 0d0a 5573 6572 2d41 6765 6e74 3a20  .8..User-Agent:.
            0x0100:  4d6f 7a69 6c6c 612f 352e 3020 284d 6163  Mozilla/5.0.(Mac
            0x0110:  696e 746f 7368 3b20 496e 7465 6c20 4d61  intosh;.Intel.Ma
            0x0120:  6320 4f53 2058 2031 305f 395f 3529 2041  c.OS.X.10_9_5).A
            0x0130:  7070 6c65 5765 624b 6974 2f35 3337 2e33  ppleWebKit/537.3
            0x0140:  3620 284b 4854 4d4c 2c20 6c69 6b65 2047  6.(KHTML,.like.G
            0x0150:  6563 6b6f 2920 4368 726f 6d65 2f33 382e  ecko).Chrome/38.
            0x0160:  302e 3231 3235 2e31 3031 2053 6166 6172  0.2125.101.Safar
            0x0170:  692f 3533 372e 3336 0d0a 4163 6365 7074  i/537.36..Accept
            0x0180:  2d45 6e63 6f64 696e 673a 2067 7a69 702c  -Encoding:.gzip,
            0x0190:  6465 666c 6174 652c 7364 6368 0d0a 4163  deflate,sdch..Ac
            0x01a0:  6365 7074 2d4c 616e 6775 6167 653a 2065  cept-Language:.e
            0x01b0:  6e2d 5553 2c65 6e3b 713d 302e 380d 0a49  n-US,en;q=0.8..I
            0x01c0:  662d 4d6f 6469 6669 6564 2d53 696e 6365  f-Modified-Since
            0x01d0:  3a20 5375 6e2c 2031 3220 4f63 7420 3230  :.Sun,.12.Oct.20
            0x01e0:  3134 2031 393a 3430 3a32 3020 474d 540d  14.19:40:20.GMT.
            0x01f0:  0a0d 0a                                  ...

### Printing packet data in ASCII only

    # tcpdump -nvvv -i any -c 1 -A 'port 80 and host 10.0.3.1'

I tend to prefer to print only the ASCII data, this helps me to quickly identify what is being sent and what is correct or not correct about the packets data. To print packet data in only the ascii format you can use the `-A` flag.

    # tcpdump -nvvv -i any -c 1 -A 'port 80 and host 10.0.3.1'
    tcpdump: listening on any, link-type LINUX_SLL (Linux cooked), capture size 65535 bytes
    19:59:52.011337 IP (tos 0x0, ttl 64, id 53757, offset 0, flags [DF], proto TCP (6), length 406)
        10.0.3.1.46172 > 10.0.3.246.80: Flags [P.], cksum 0x1c7f (incorrect -> 0xead1), seq 1552520173:1552520527, ack 428165415, win 237, options [nop,nop,TS val 624251177 ecr 624247749], length 354
    E.....@.@.Ln
    ...
    ....\.P\.....I'...........
    %5Q)%5C.GET /newpage HTTP/1.1
    Host: 10.0.3.246
    Connection: keep-alive
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36
    Accept-Encoding: gzip,deflate,sdch
    Accept-Language: en-US,en;q=0.8

As you can see from the output above we have successfully captured an http `GET` request. Being able to print the packet data in a human readable format is very useful when troubleshooting application issues where the traffic is not encrypted. If you are troubleshooting encrypted traffic then printing packet data is not very useful. However, if you use have the certificates in use you could use commands such as `ssldump` or even `wireshark`.

## Non-TCP Traffic

While the majority of this article covered TCP based traffic `tcpdump` can capture much more than TCP. It can also be used to capture ICMP, UDP, and ARP packets to name a few. Below are a few quick examples of non-TCP packets captured by `tcpdump`.

### ICMP packets

    # tcpdump -nvvv -i any -c 2 icmp
    tcpdump: listening on any, link-type LINUX_SLL (Linux cooked), capture size 65535 bytes
    20:11:24.627824 IP (tos 0x0, ttl 64, id 0, offset 0, flags [DF], proto ICMP (1), length 84)
        10.0.3.169 > 10.0.3.246: ICMP echo request, id 15683, seq 1, length 64
    20:11:24.627926 IP (tos 0x0, ttl 64, id 31312, offset 0, flags [none], proto ICMP (1), length 84)
        10.0.3.246 > 10.0.3.169: ICMP echo reply, id 15683, seq 1, length 64

### UDP packets

    # tcpdump -nvvv -i any -c 2 udp
    tcpdump: listening on any, link-type LINUX_SLL (Linux cooked), capture size 65535 bytes
    20:12:41.726355 IP (tos 0xc0, ttl 64, id 0, offset 0, flags [DF], proto UDP (17), length 76)
        10.0.3.246.123 > 198.55.111.50.123: [bad udp cksum 0x43a9 -> 0x7043!] NTPv4, length 48
            Client, Leap indicator: clock unsynchronized (192), Stratum 2 (secondary reference), poll 6 (64s), precision -22
            Root Delay: 0.085678, Root dispersion: 57.141830, Reference-ID: 199.102.46.75
              Reference Timestamp:  3622133515.811991035 (2014/10/12 20:11:55)
              Originator Timestamp: 3622133553.828614115 (2014/10/12 20:12:33)
              Receive Timestamp:    3622133496.748308420 (2014/10/12 20:11:36)
              Transmit Timestamp:   3622133561.726278364 (2014/10/12 20:12:41)
                Originator - Receive Timestamp:  -57.080305658
                Originator - Transmit Timestamp: +7.897664248
    20:12:41.748948 IP (tos 0x0, ttl 54, id 9285, offset 0, flags [none], proto UDP (17), length 76)
        198.55.111.50.123 > 10.0.3.246.123: [udp sum ok] NTPv4, length 48
            Server, Leap indicator:  (0), Stratum 3 (secondary reference), poll 6 (64s), precision -20
            Root Delay: 0.054077, Root dispersion: 0.058944, Reference-ID: 216.229.0.50
              Reference Timestamp:  3622132887.136984840 (2014/10/12 20:01:27)
              Originator Timestamp: 3622133561.726278364 (2014/10/12 20:12:41)
              Receive Timestamp:    3622133618.830113530 (2014/10/12 20:13:38)
              Transmit Timestamp:   3622133618.830129086 (2014/10/12 20:13:38)
                Originator - Receive Timestamp:  +57.103835195
                Originator - Transmit Timestamp: +57.103850722

If you have an awesome `tcpdump` command example that you think should be added to this article feel free to post it in the comments section.

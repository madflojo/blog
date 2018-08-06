---
authors:
- Benjamin Cane
categories:
- Linux
date: '2016-05-18T03:30:00'
description: What is swap, and how to use a swap file to add memory to low memory
  cloud servers
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- swap
- linux memory
- performance
- cloud servers
- low memory
- docker memory
title: Creating a swap file for tiny cloud servers
url: /2016/05/18/creating-a-swap-file-for-tiny-cloud-servers

---
A few months ago while setting up a few cloud servers to host one of my applications. I started running into an interesting issue while building Docker containers. During the `docker build` execution my servers ran out of memory causing the Docker build to fail.

The servers in question only have about `512MB` of RAM and the Docker execution was using the majority of the available memory. My solution to this problem was simple, add a swap file.

A swap file is a file that lives on a file system and is used like a swap device.

While adding the swap file I thought this would make for an interesting article. Today's post is going to cover how to add a swap file to a Linux system. However, before we jump into creating a swap file, let's explore what exactly swap is and how it works.

## What is swap

When Linux writes data to physical memory, or RAM it does so in chunks that are called **pages**. Pages can vary in size from system to system but in general a page is a small amount of data. The Linux kernel will keep these pages in physical memory for as long as it has available memory to spare and the pages are relevant.

When the kernel needs to make room for new memory pages it will move some memory pages out of physical memory, where the destination is usually to a swap device. Swap devices are hard-drive partitions or files within a file system used to expand the memory capacity of a system.

A simple way to think of swap is to think of it as an overflow area for system memory. With that thought, the general rule of thumb is that memory pages being written to swap is a bad thing. In my case however, since the only time I require swap is during the initial build of my Docker containers. Swapping isn't necessarily a bad thing.

In fact, my use case is exactly the reason why swap exists. I have a process that requires more memory than what is available on my system, and I would prefer to use some disk space to perform the task rather than add memory to the system. The key is that my system does not swap during normal operations, only during the Docker build execution.

### Determining if a system is Swapping

In summary, Swapping is only a bad thing, if it happens during unexpected times. A simple way to determine if a system is actively swapping is to run the `vmstat` command.

```
$ vmstat -n 5 5
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 0  0    100 207964  22056 129964    0    0    14     1   16   32  0  0 100  0  0
 0  0    100 207956  22056 129956    0    0     0     0   16   26  0  0 100  0  0
 0  0    100 207956  22064 129956    0    0     0     2   16   27  0  0 100  0  0
 0  0    100 207956  22064 129956    0    0     0     0   14   23  0  0 100  0  0
 0  0    100 207956  22064 129956    0    0     0     0   14   24  0  0 100  0  0
```

The `vmstat` command can be used to show memory statistics from the system in question. In the above there are two columns, `si` (Swapped In) and `so` (Swapped Out) which are used to show the number of pages swapped in and swapped out.

Since the output above shows that the example system is neither swapping in, or swapping out memory pages, we can assume that swapping on this server is probably not an issue. The fact that at one point the system has swapped `100KB` of data does not necessarily mean there is an issue.

### When does a system swap

A common misconception about swap and Linux is that the system will swap only when it is completely out of memory. While this was mostly true a long time ago, recent versions of the Linux kernel include a tunable parameter called `vm.swappiness`. The `vm.swappiness` parameter is essentially an aggressiveness setting. The higher the `vm.swappiness` value (`0` - `100`), the more aggressive the kernel will swap. When set to `0`, the kernel will only swap once the system memory is below the `vm.min_free_kbytes` value.

What this means is, unless `vm.swappiness` is set at `0`. The system may swap at any time, even without memory being completely used. Since by default the `vm.swappiness` value is set to `60`, which is somewhat on the aggressive side. A typical Linux system may swap without ever hitting the `vm.min_free_kbytes` threshold.

This aggressiveness does not often impact performance (though it can in some cases) because when the kernel decides to start swapping it will pick memory pages based on the last accessed time of those pages. What this means is, data that is frequently accessed is kept in physical memory longer, and data that is not frequently accessed is usually the primary candidates for moving to swap.

Now that we have a better understanding of swap, let's add a swap device to the cloud servers in question.

## Adding a swap device

Adding a swap device is fairly easy and can be done with only a few commands. Let's take a look at the memory available on the system today. We will do this with the `free` command, using the `-m` (Megabytes) flag.

```
$ free -m
             total       used       free     shared    buffers     cached
Mem:           489        281        208          0         17        126
-/+ buffers/cache:        136        353
Swap:            0          0          0
```

From the `free` command's output we can see that this server currently has no swap space at all. We will change that by creating a `2GB` swap file.

### Creating a swap file

The first step in creating a swap file is to create a file with the `dd` command.

```
$ sudo dd if=/dev/zero of=/swap bs=1M count=2048
2048+0 records in
2048+0 records out
2147483648 bytes (2.1 GB) copied, 5.43507 s, 395 MB/s
```

The reason we used `dd` to create the file is because we can create more than a simple empty file. With the `dd` command above we created a `2GB` file (writing `1MB` chunks `2048` times) with the contents being populated from `/dev/zero`. This gives us the data space that will make up the swap device. Whatever size we make the file in this step, is the size the swap device will be.

With the file created, we can now use the `mkswap` command to make the file a swap device.

```
$ sudo mkswap /swap
Setting up swapspace version 1, size = 2097148 KiB
no label, UUID=0d64a557-b7f9-407e-a0ef-d32ccd081f4c
```

The `mkswap` command is used to setup a file or device as a swap device. This is performed by formatting the device or file as a swap partition.

### Mounting the swap device

With our file now formatted as a swap device we can start the steps to mount it. Like any other filesystem device, in order to mount our swap device we will need to specify it within the `/etc/fstab` file. Let's start by appending the below contents into the `/etc/fstab` file.

```
/swap   swap  swap  defaults  0 0
```

With the above step complete, we can now mount the swap file. To do this we will use the `swapon` command.

```sh
$ sudo swapon -a
```

The `-a` flag for `swapon` tells the command to mount and activate all defined swap devices within the `/etc/fstab` file. To check if our swap file was successfully mounted we can execute the `swapon` command again with the `-s` option.

```
$ sudo swapon -s
Filename				Type		Size	Used	Priority
/swap                                   file		2097148	0	-1
```

From the above we can see that `/swap`, the file we created is mounted and currently in use as a swap device. If we were to re-run the `free` command from above we should also see the swap space available.

```
$ free -m
             total       used       free     shared    buffers     cached
Mem:           489        442         47          0         11        291
-/+ buffers/cache:        139        350
Swap:         2047          0       2047
```

In the previous execution of the `free` command the swap size was `0` and now it is `2047 MB`. This means we have roughly `2GB` of swap to use with this system.

A useful thing to know about Linux is that you can have multiple swap devices. The `priority` value of the swap device is used to determine in what order the data should be written. When 2 or more swap devices have the same `priority` swap usage is balanced across both. This means you can gain some performance during times of swap usage by creating multiple swap devices on different hard-drives.

Got any other swap tips? Add them below in the comments.

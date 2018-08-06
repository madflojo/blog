---
authors:
- Benjamin Cane
categories:
- Administration
- Best Practices
- Linux
date: '2011-07-07T03:21:00'
draft: false
header:
  caption: ''
  image: ''
tags:
- kernel
- linkedin
- linux
- tech
- unix
title: 'oom-killer: If you see this you should reboot'
url: /2011/07/07/oom-killer-if-you-see-this-you-should-reboot

---

If you have ever run a system with very little memory such as a small virtual server *cough* or a server with a java application *cough* than you might have seen this type of error every now and then.

     Jul 611:39:55 slize kernel: [1262223.326537] apache2 invoked oom-killer: gfp_mask=0x200da, order=0, oom_adj=0

## What is oom-killer?

oom-killer is a process that the kernel will call when a system is over committed on memory. This will only be invoked if your system has exhausted both physical and swap memory. If this happens oom-killer will launch and start to kill processes based on a naughty score which can be found in `/proc/<PID>/oom_score`.

    $ cat /proc/1678/oom_score
    315

oom-killer will kill processes with the highest score first, generally targeting processes that are using up the most cpu and memory, but there are ways of adjusting this (a topic for later).

## Wait, What? Reboot?

So what should you do if you see oom-killer? In short you should reboot. I know it feels a little dirty to reboot a linux server but in reality its probably the easiest and best way to respond to oom-killer.

Let me explain why.

oom-killer can be told not to kill certain processes but aside from that, it is pretty indiscriminate about what it kills and you have to do that in advance. It may kill your application or it may kill necessary system processes, you never really know. Unless you keep a list of all your system processes do you really know for certain that you restarted all of the necessary processes? Not likely.

oom-killer will log what it kills through syslog but keep in mind, oom-killer is launched because your system is running out of memory. The integrity of what has been logged is in question.

While your gut reaction might be to never reboot a linux machine in the case of oom-killer it is the easiest way to guarantee that all of the necessary processes are running and running correctly.

I do want to point out that a reboot is not always possible in certain environments; I still think rebooting is the proper answer so you must ask yourself is it better to plan the reboot or it reboot itself randomly?

### Reddit Note:

After reading some Reddit notes linking to this article I should probably clarify, before you reboot the server **you should troubleshoot what is causing your system to run out of memory** and swap otherwise the issue will reoccur. Now with that said, I still believe that the right thing to do is to reboot your server before putting it back into service or calling it good. oom-killer may have killed vital services on your system and by vital I mean important to the function of that server and the services that run on it; sure you could go through logs and try and figure out everything but what happens if you miss something?


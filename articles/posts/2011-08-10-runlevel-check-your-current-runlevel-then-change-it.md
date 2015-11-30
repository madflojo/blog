
Today's commands are how you can check what runlevel your system is in and then change it.

**Check the current runlevel:**

    [root@bcane tmp]# runlevel   
    N 5

**Change the current runlevel:**

    [root@bcane tmp]# init <new_level>

The run levels in Unix/Linux are used to define what state init (the parent of all processes) is in. Each distribution of Unix/Linux has different definitions of what run levels starts what processes.

Usually you can find the different definitions in `/etc/inittab` below is the one from a fedora box.

    # Default runlevel. The runlevels used are:  
    # 0 - halt (Do NOT set initdefault to this)  
    # 1 - Single user mode  
    # 2 - Multiuser, without NFS (The same as 3, if you do not have networking)  
    # 3 - Full multiuser mode  
    # 4 - unused  
    # 5 - X11  
    # 6 - reboot (Do NOT set initdefault to this)




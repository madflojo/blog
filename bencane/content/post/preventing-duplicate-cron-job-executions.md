---
authors:
- Benjamin Cane
categories:
- Bash Scripting
- Cron jobs
date: '2015-09-22T13:20:00'
description: This article will show both BASH code and utilities that can be used
  to prevent a cron job from having multiple running instances
draft: false
header:
  caption: ''
  image: ''
tags:
- bash
- shell scripting
- cron
- cronjob
- cron jobs
- scheduling
- duplicate scripts
- sh
- shell
- scripting
- cron scripts
- lock file
- pid file
- pidfile
- flock
title: Preventing duplicate cron job executions
url: /2015/09/22/preventing-duplicate-cron-job-executions

---

I feel like sometimes cron jobs create more problems than they solve. It's not the fault of cron, but rather the jobs being executed. This is especially true when the jobs result in duplicate running instances like the following example.

    $ ps -elf | grep forever
    4 S vagrant   4095  4094  0  80   0 -  1111 wait   21:59 ?        00:00:00 /bin/sh -c /var/tmp/forever.sh
    0 S vagrant   4096  4095  0  80   0 -  2779 wait   21:59 ?        00:00:00 /bin/bash /var/tmp/forever.sh
    4 S vagrant   4100  4099  0  80   0 -  1111 wait   22:00 ?        00:00:00 /bin/sh -c /var/tmp/forever.sh
    0 S vagrant   4101  4100  0  80   0 -  2779 wait   22:00 ?        00:00:00 /bin/bash /var/tmp/forever.sh
    4 S vagrant   4130  4129  0  80   0 -  1111 wait   22:01 ?        00:00:00 /bin/sh -c /var/tmp/forever.sh
    0 S vagrant   4131  4130  0  80   0 -  2779 wait   22:01 ?        00:00:00 /bin/bash /var/tmp/forever.sh
    4 S vagrant   4135  4134  0  80   0 -  1111 wait   22:02 ?        00:00:00 /bin/sh -c /var/tmp/forever.sh
    0 S vagrant   4136  4135  0  80   0 -  2779 wait   22:02 ?        00:00:00 /bin/bash /var/tmp/forever.sh

The above is actually a fairly common problem. Someone writes a script, creates a cron job to execute that script and the script works great, **at first**. Over time, something changes and the script either starts to take a long time to execute or never completes. The fact that the script never ends is one problem, the other problem is that scripts like the one above keep starting even though another instance of that same script is running.

In today's article we are going to cover ways to solve the second issue by preventing duplicate cron job executions.

## Methods of preventing duplicates

Whether it's performed by a tool or coding there are 2 common techniques used to prevent duplicate cron job executions; **lock files** and **PID files**.

* Lock file

The first technique is a **lock file**. A common implementation of this is to simply check if a file exists, if it does, stop the job execution. If the file does not exist, than create it and continue executing the job.

* PID file

The second technique is a **PID file** or Process ID file. The **PID file** method is similar to a **lock file** except that within the file is the process ID of the running instance. The process ID can then be used to validate that the process is still running.

Of the above methods, the **PID file** is the better option. The reason I believe this is due to limitations of the **lock file** method described above. When a script is only checking for a file's existence there is no validation that the process is still running. If the process was killed or abnormally terminated without removing the **lock file**, the job in question would not run again until someone or something cleaned up the **lock file**.

With that said, there are ways to utilize a **lock file** beyond a simple "does this file exist" method. I will cover this while discussing utilities towards the end of this article.

## How to create a PID file in BASH

Since the **PID file** method is often easier to implement I will show some best practices for creating and maintaining a **PID file** in BASH scripts.

### Modifying an existing script

For this example there is already a script that has duplicate cron executions (`forever.sh`), we will use this script to show how to manage a **PID file**.

    #!/bin/bash
    sleep 25d

The script is pretty simple, after starting it will `sleep` for 25 days and then exit. Since this job is launched every minute it comes as no surprise that there are duplicate instances running.

#### Defining the PID file

The first thing we will add to this script is a variable defining the location of our **PID file**.

    PIDFILE=/home/vagrant/forever.pid

This first step is pretty simple but also problematic if done wrong. For the most part, the location of the **PID file** doesn't matter; however, what does matter is that the **PID file** should never be located within `/var/tmp/` or `/tmp/`. The reason for this is because these directories are temporary directories which have their contents "cleaned up" after a certain amount of time.

On Ubuntu the `/tmp/` directory is cleaned up on reboot, which means this shouldn't be a problem. However, on Red Hat Enterprise Linux the `/tmp/` directory is cleaned daily where files that haven't been used for a specific time-frame are removed.

In addition to automatic deletions, the `/tmp/` directory's contents are considered temporary and it is not unheard of for a **PID file** in `/tmp/` to mysteriously disappear. On systems with many users the `/tmp/` and `/var/tmp/` directories are often overcrowded and sometimes manually "purged". This process can sometimes lead to a **PID file** being erroneously removed. 

If the **PID file** is removed, the next execution of the script will simply believe there is no job running, causing duplicate instances.

For this example, we can put the **PID file** in our home directory.

#### Checking for the PID file's existence

Since we now have a defined **PID file** we can check for it's existence with a fairly simple BASH `if` statement.

    PIDFILE=/home/vagrant/forever.pid
    if [ -f $PIDFILE ]
    then
      # do something
    fi

The above `if` statement simply checks if the value of `$PIDFILE` is a file with the `-f` test. If the file exists the `if` statement will be true and execute what is between `then` and `fi`.

#### What to do if the PID file doesn't exist

If the **PID file** doesn't exist we will want to execute our code but before we do that we also need to create a **PID file** to prevent other instances from executing. Since the **PID file** existence is already being checked with the `if` statement we can use this same statement to identify when we should create a **PID file**.

We can do this by adding an `else` to the `if` statement.

    PIDFILE=/home/vagrant/forever.pid
    if [ -f $PIDFILE ]
    then
      # do something
    else
      echo $$ > $PIDFILE
      if [ $? -ne 0 ]
      then
        echo "Could not create PID file"
        exit 1
      fi
    fi

The above is a bit more than just creating a **PID file**. Let's break this down a bit. 

      echo $$ > $PIDFILE

The above line will not only create the **PID file** but also write the process ID of this job into that file. It does this by using `echo` to print the value of `$$` and redirect (`>`) it to `$PIDFILE`. The `$$` variable, is a special variable within BASH that returns the current process ID.

    $ echo $$
    11158

The above is a very simple way of populating the **PID file** with the appropriate process ID, but what happens if this `echo` fails?

      if [ $? -ne 0 ]
      then
        echo "Could not create PID file"
        exit 1
      fi

That's where the second `if` statement comes in handy. The above `if` statement will check the `echo` command's [exit code](http://bencane.com/2014/09/02/understanding-exit-codes-and-how-to-use-them-in-bash-scripts/). If the `echo` was not successful it will `print` an error and `exit` with an exit code indicating error.

Since I covered testing for exit codes in a [previous article](http://bencane.com/2014/09/02/understanding-exit-codes-and-how-to-use-them-in-bash-scripts/) we will refrain from digging too deep on this last `if` block.

#### Double checking the process is actually running

Many times I've seen shell scripts simply check if the **PID file** exists and exit. This defeats the purpose of a **PID file** containing the process ID and makes it no different than a **lock file**.

For our example we will do more than assume the process is running.

    PIDFILE=/home/vagrant/forever.pid
    if [ -f $PIDFILE ]
    then
      PID=$(cat $PIDFILE)
      ps -p $PID > /dev/null 2>&1
      if [ $? -eq 0 ]
      then
        echo "Job is already running"
        exit 1
      else
        ## Process not found assume not running
        echo $$ > $PIDFILE
        if [ $? -ne 0 ]
        then
          echo "Could not create PID file"
          exit 1
        fi
      fi
    else
      echo $$ > $PIDFILE
      if [ $? -ne 0 ]
      then
        echo "Could not create PID file"
        exit 1
      fi
    fi

In the above we added a few lines of code to help identify if there really is another instance of this script running. Let's break these down to get a better understanding of what is happening.

      PID=$(cat $PIDFILE)
      ps -p $PID > /dev/null 2>&1

The first two lines are pretty simple. The first will read the **PID file** with the `cat` command and assign the output to the variable `$PID`. The second line will execute a `ps` using the `-p` (process) flag specifying the process ID to search for; the value of `$PID`.

The next block of code is a bit more complex.

      if [ $? -eq 0 ]
      then
        echo "Job is already running"
        exit 1
      else
        ## Process not found assume not running
        echo $$ > $PIDFILE
        if [ $? -ne 0 ]
        then
          echo "Could not create PID file"
          exit 1
        fi
      fi

Again we are using the `$?` special variable to check the exit code of the last command executed. In this case the `ps` command. If the `ps` command successfully finds a process with the process ID provided it will exit with a `0` exit code. If the `ps` command does not find the specified process ID it will exit with a `1`.

In the above `if` statement we check if the exit code for `ps` is `0`, if it is we simply print that the **"Job is already running"** and exit with a value of `1`; showing error. If the exit code of the `ps` command is anything but `0` however, we once again create a **PID file** and continue executing the script (also checking if the **PID file** creation is successful).

#### Cleaning up

Since we are checking if the previous **PID file** process is running we could simply leave the **PID file** in place between executions. However, that would be a bit lazy, potentially cause issues and not something to be encouraged. Especially when cleaning up can be a simple `rm` command.

    rm $PIDFILE

Adding the above `rm` command to the end of the script will result in cleaning up the **PID file** after a successful execution. If the script exits any other places this step should be included before the `exit` command.

### Summary of Changes

Now that we have made our changes let's take another look at this script.

    #!/bin/bash
    
    PIDFILE=/home/vagrant/forever.pid
    if [ -f $PIDFILE ]
    then
      PID=$(cat $PIDFILE)
      ps -p $PID > /dev/null 2>&1
      if [ $? -eq 0 ]
      then
        echo "Process already running"
        exit 1
      else
        ## Process not found assume not running
        echo $$ > $PIDFILE
        if [ $? -ne 0 ]
        then
          echo "Could not create PID file"
          exit 1
        fi
      fi
    else
      echo $$ > $PIDFILE
      if [ $? -ne 0 ]
      then
        echo "Could not create PID file"
        exit 1
      fi
    fi
    
    sleep 25d
    rm $PIDFILE

If we run the same script from command line we should see that we are no longer able to execute more than one instance at a time.

    $ /var/tmp/forever.sh &
    [1] 7073
    $ /var/tmp/forever.sh 
    Process already running

If we kill the first copy however (which means the **PID file** will still exist) we should be able to launch another instance.

    $ kill 7073
    $ /var/tmp/forever.sh 

The code above is a useful method for managing a **PID file** within BASH. This method will prevent duplicate instances from running as well as handle scenarios where a **PID file** exists even though the script is not actually running. There is one scenario however that this method does not account for. 

If the process is killed and another process uses the same process ID as the original. It is possible in this scenario that the job would not run since the process ID is in use. This scenario is an edge case but it is entirely possible. The below utilities help solve this.

## Utilities

Sometimes it is not possible to modify the code being executed by a cron job or you may simply want a quick fix for this type of issue. For these scenarios there are two utilities that I recommend `flock` and `solo`.

### The flock command

The `flock` command is installed by default on newer Linux distributions and is useful for utilizing the **lock file** method, however unlike many implementations it does more than check if the file exists.

To get started let's look at using `flock` to prevent multiple instances of our script. To do this we could call our script as per below.

    $ flock -xn /home/vagrant/forever.lck -c /var/tmp/forever.sh

The above `flock` command will open the `/home/vagrant/forever.lck` file with an exclusive (`-x`) file lock and execute the specified command (`-c`). If we run a second instance `flock` will identify there is already an exclusive file lock.

    $ flock -xn /home/vagrant/forever.lck -c /var/tmp/forever.sh 
    $ echo $?
    1

When `flock` cannot lock a file and it is executed with the `-n` (non-blocking) flag, the `flock` command will exit silently with an exit code that indicates an error has occurred. 

The useful thing about `flock` is that the file lock will be kept in place until the original process completes, at that point `flock` will release the file lock. This is true whether the process completes successfully or unsuccessfully.

### The solo program

[Solo](http://timkay.com/solo/) is actually a program I found while looking for a way to ensure I didn't run into this same issue with a long running application task. Solo is a Perl script that works similar to `flock` however rather than relying on a lock file the `solo` program binds a port.

    $ ./solo -port=6000 /var/tmp/forever.sh &
    [1] 7503
    $ ./solo -port=6000 /var/tmp/forever.sh
    solo(6000): Address already in use

When executed `solo` will bind the specified port and execute the specified command. Once the command is finished the port is released allowing the next invocation of the job to execute normally.

Of these two utilities I personally like `solo` the best. The thing I like most about `solo` is that no one can remove a file and accidentally cause duplicate instances to run. Even with the `flock` command if the underlying file is removed a second job can be initiated. Since `solo` binds a port it is not possible for someone to accidentally allow a second instance of the job to run.

## Detecting issues

The above utilities and best practices are very useful for preventing duplicate jobs. However, when a cron job does go rouge these utilities do not stop that job from running a prolonged amount of time. The best thing to do for this scenario is to simply monitor the length of time it takes each job. There are a number of services out there that perform cron job monitoring, one that I have used and like is [Cronitor](https://cronitor.io).

These tools often work by performing an HTTP request before and after the job's execution to track the length of time each job takes. The nice thing is, these tools will also alert if a job has not run within a defined time period.

## Final thoughts

In the above I covered several methods for preventing duplicate cron job executions. While this problem may by simple to solve with a little bit of code or a utility, these are often overlooked and never addressed until it becomes a serious problem. I highly suggest anyone running into this scenario to correct the issue right away, if left unchecked duplicate jobs can often lead to serious issues.

Issues such as consuming the maximum number of open files, consuming the maximum number of process id's, or simply utilizing all of a systems CPU or memory. Any of these 3 could spell disaster for a production environment.

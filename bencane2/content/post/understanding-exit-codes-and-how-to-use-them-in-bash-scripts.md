---
authors:
- Benjamin Cane
categories:
- Linux
- Scripting
date: '2014-09-02T14:45:00'
description: When writing a script that calls other commands, how do you know if they
  were successful or not? The answer is exit codes, exit codes are important and this
  article describes how to use them in your scripts and understand them in general.
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- unix
- freebsd
- bash
- advanced bash scripting
- bash scripting
- bash exit codes
- bash shell scripting
- bash examples
title: Understanding Exit Codes and how to use them in bash scripts
url: /2014/09/02/understanding-exit-codes-and-how-to-use-them-in-bash-scripts

---

Lately I've been working on a lot of automation and monitoring projects, a big part of these projects are taking existing scripts and modifying them to be useful for automation and monitoring tools. One thing I have noticed is sometimes scripts use exit codes and sometimes they don't. It seems like exit codes are easy for poeple to forget, but they are an incredibly important part of any script. Especially if that script is used for the command line.

## What are exit codes?

On Unix and Linux systems, programs can pass a value to their parent process while terminating. This value is referred to as an exit code or exit status. On POSIX systems the standard convention is for the program to pass `0` for successful executions and `1` or higher for failed executions.

Why is this important? If you look at exit codes in the context of scripts written to be used for the command line the answer is very simple. Any script that is useful in some fashion will inevitably be either used in another script, or wrapped with a bash one liner. This becomes especially true if the script is used with automation tools like SaltStack or monitoring tools like Nagios, these programs will execute scripts and check the status code to determine whether that script was successful or not. 

On top of those reasons, exit codes exist within your scripts even if you don't define them. By not defining proper exit codes you could be falsely reporting successful executions which can cause issues depending on what the script does.

### What happens if I don't specify an exit code

In Linux any script run from the command line has an exit code. With Bash scripts, if the exit code is not specified in the script itself the exit code used will be the exit code of the last command run. To help explain exit codes a little better we are going to use a quick sample script.

**Sample Script:**

    #!/bin/bash
    touch /root/test
    echo created file

The above sample script will execute both the `touch` command and the `echo` command. When we execute this script (as a non-root user) the touch command will fail, ideally since the touch command failed we would want the exit code of the script to indicate failure with an appropriate exit code. To check the exit code we can simply print the `$?` special variable in bash. This variable will print the exit code of the last run command.

**Execution:**

    $ ./tmp.sh 
    touch: cannot touch '/root/test': Permission denied
    created file
    $ echo $?
    0

As you can see after running the `./tmp.sh` command the exit code was `0` which indicates success, even though the touch command failed. The sample script runs two commands `touch` and `echo`, since we did not specify an exit code the script exits with the exit code of the last run command. In this case, the last run command is the `echo` command, which did execute successfully.

**Script:**

    #!/bin/bash
    touch /root/test

If we remove the `echo` command from the script we should see the exit code of the `touch` command.

**Execution:**

    $ ./tmp.sh 
    touch: cannot touch '/root/test': Permission denied
    $ echo $?
    1

As you can see, since the last command run was `touch` the exit code reflects the true status of the script; failed.

## Using exit codes in your bash scripts

While removing the `echo` command from our sample script worked to provide an exit code, what happens when we want to perform one action if the `touch` was successful and another if it was not. Actions such as printing to `stdout` on success and `stderr` on failure.

### Testing for exit codes

Earlier we used the `$?` special variable to print the exit code of the script. We can also use this variable within our script to test if the `touch` command was successful or not. 

**Script:**

    #!/bin/bash
    
    touch /root/test 2> /dev/null
    
    if [ $? -eq 0 ]
    then
      echo "Successfully created file"
    else
      echo "Could not create file" >&2
    fi

In the above revision of our sample script; if the exit code for `touch` is `0` the script will `echo` a successful message. If the exit code is anything other than `0` this indicates failure and the script will `echo` a failure message to `stderr`.

**Execution:**

    $ ./tmp.sh
    Could not create file

### Providing your own exit code

While the above revision will provide an error message if the `touch` command fails, it still provides a `0` exit code indicating success.

    $ ./tmp.sh
    Could not create file
    $ echo $?
    0

Since the script failed, it would not be a good idea to pass a successful exit code to any other program executing this script. To add our own exit code to this script, we can simply use the `exit` command.

**Script:**

    #!/bin/bash
  
    touch /root/test 2> /dev/null
    
    if [ $? -eq 0 ]
    then
      echo "Successfully created file"
      exit 0
    else
      echo "Could not create file" >&2
      exit 1
    fi

With the `exit` command in this script, we will exit with a successful message and `0` exit code if the `touch` command is successful. If the `touch` command fails however, we will print a failure message to `stderr` and exit with a `1` value which indicates failure.

**Execution:**

    $ ./tmp.sh
    Could not create file
    $ echo $?
    1

### Using exit codes on the command line

Now that our script is able to tell both users and programs whether it finished successfully or unsuccessfully we can use this script with other administration tools or simply use it with bash one liners.

**Bash One Liner:**

    $ ./tmp.sh && echo "bam" || (sudo ./tmp.sh && echo "bam" || echo "fail")
    Could not create file
    Successfully created file
    bam

The above grouping of commands use what is called **list constructs** in bash. List constructs allow you to chain commands together with simple `&&` for **and** and `||` for **or** conditions. The above command will execute the `./tmp.sh` script, and if the exit code is `0` the command `echo "bam"` will be executed. If the exit code of `./tmp.sh` is `1` however, the commands within the parenthesis will be executed next. Within the parenthesis the commands are chained together using the `&&` and `||` constructs again. 

The list constructs use exit codes to understand whether a command has successfully executed or not. If scripts do not properly use exit codes, any user of those scripts who use more advanced commands such as list constructs will get unexpected results on failures.

### More exit codes

The `exit` command in bash accepts integers from `0 - 255`, in most cases `0` and `1` will suffice however there are other reserved exit codes that can be used for more specific errors. The Linux Documentation Project has a pretty good table of [reserved exit codes](http://www.tldp.org/LDP/abs/html/exitcodes.html) and what they are used for.
